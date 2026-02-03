from flask import Flask, render_template, request, jsonify
import csv
import io
import os
import json
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

# Path to persistent stats file on VPS
STATS_FILE = 'usage_stats.json'

def get_stats():
    if not os.path.exists(STATS_FILE):
        return {"files_processed": 0, "products_updated": 0, "images_added": 0, "total_usage_count": 0}
    with open(STATS_FILE, 'r') as f:
        return json.load(f)

def update_stats(new_products, new_images):
    stats = get_stats()
    stats["files_processed"] += 1
    stats["products_updated"] += new_products
    stats["images_added"] += new_images
    stats["total_usage_count"] += 1
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f)

@app.route('/')
def index():
    return render_template('index.html', stats=get_stats())

@app.route('/api/stats')
def api_stats():
    return jsonify(get_stats())

@app.route('/process', methods=['POST'])
def process_csv():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        image_url = request.form.get('imageUrl', '').strip()
        alt_text = request.form.get('altText', '').strip()

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not image_url:
            return jsonify({"error": "Please provide an Image URL."}), 400

        if not (image_url.startswith('http://') or image_url.startswith('https://')):
            return jsonify({"error": "Invalid Image URL."}), 400

        # Read CSV content
        content = file.read().decode('utf-8-sig')
        stream = io.StringIO(content)
        reader = csv.DictReader(stream)
        fieldnames = reader.fieldnames

        if not fieldnames or "Handle" not in fieldnames:
            return jsonify({"error": "Invalid Shopify CSV: 'Handle' column not found."}), 400

        has_alt_col = "Image Alt Text" in fieldnames
        product_groups = defaultdict(list)
        handle_order = []
        
        for row in reader:
            handle = row.get("Handle", "")
            if not handle: continue
            if handle not in product_groups:
                handle_order.append(handle)
            product_groups[handle].append(row)

        final_rows = []
        added_count = 0
        skipped_count = 0

        for handle in handle_order:
            rows = product_groups[handle]
            max_pos = 0
            image_exists = False
            for row in rows:
                pos_val = row.get("Image Position")
                if pos_val and str(pos_val).isdigit():
                    max_pos = max(max_pos, int(pos_val))
                if row.get("Image Src") == image_url:
                    image_exists = True
            
            final_rows.extend(rows)
            
            if image_exists:
                skipped_count += 1
            else:
                new_row = {field: "" for field in fieldnames}
                new_row["Handle"] = handle
                new_row["Image Src"] = image_url
                new_row["Image Position"] = str(max_pos + 1)
                if has_alt_col:
                    new_row["Image Alt Text"] = alt_text
                
                final_rows.append(new_row)
                added_count += 1

        # Update global stats
        update_stats(len(handle_order), added_count)

        output_stream = io.StringIO()
        writer = csv.DictWriter(output_stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_rows)
        
        return jsonify({
            "success": True,
            "stats": {
                "totalProducts": len(handle_order),
                "added": added_count,
                "skipped": skipped_count,
                "totalRows": len(final_rows)
            },
            "global_stats": get_stats(),
            "csvContent": output_stream.getvalue(),
            "fileName": f"processed_{file.filename}"
        })

    except Exception as e:
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

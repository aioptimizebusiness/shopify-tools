from flask import Flask, render_template, request, jsonify, send_from_directory
import csv
import io
import os
import json
from datetime import datetime

app = Flask(__name__)

# Constants
STATS_FILE = 'usage_stats.json'

def get_stats():
    if not os.path.exists(STATS_FILE):
        return {"files_processed": 0, "products_updated": 0, "images_added": 0, "total_usage_count": 0}
    try:
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"files_processed": 0, "products_updated": 0, "images_added": 0, "total_usage_count": 0}

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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.webp', mimetype='image/webp')

@app.errorhandler(404)
def page_not_found(e):
    # Simply redirect to index for micro-apps hub or show simple 404
    return render_template('index.html', stats=get_stats()), 404

@app.route('/process', methods=['POST'])
def process_csv():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        image_url = request.form.get('imageUrl', '').strip()
        alt_text = request.form.get('altText', '').strip()

        if not file or not file.filename.endswith('.csv'):
            return jsonify({"error": "Please upload a valid CSV file"}), 400
        
        if not image_url.startswith('http'):
            return jsonify({"error": "Invalid Image URL. Must start with http/https."}), 400

        # Read CSV
        stream = io.StringIO(file.stream.read().decode("utf-8-sig"), newline=None)
        reader = csv.DictReader(stream)
        rows = list(reader)
        
        if not rows:
            return jsonify({"error": "CSV file is empty"}), 400

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=reader.fieldnames)
        writer.writeheader()

        processed_products = set()
        added_count = 0
        skipped_count = 0
        
        handle_order = []
        product_map = {}

        for row in rows:
            h = row.get('Handle', '').strip()
            if not h: continue
            if h not in product_map:
                handle_order.append(h)
                product_map[h] = []
            product_map[h].append(row)

        for handle in handle_order:
            p_rows = product_map[handle]
            
            existing_images = [r.get('Image Src', '') for r in p_rows if r.get('Image Src')]
            max_pos = 0
            for r in p_rows:
                try:
                    pos = int(r.get('Image Position', 0))
                    if pos > max_pos: max_pos = pos
                except: continue

            if image_url in existing_images:
                skipped_count += 1
                for r in p_rows: writer.writerow(r)
            else:
                added_count += 1
                for r in p_rows: writer.writerow(r)
                
                new_row = {k: '' for k in reader.fieldnames}
                new_row['Handle'] = handle
                new_row['Image Src'] = image_url
                new_row['Image Position'] = max_pos + 1
                if 'Image Alt Text' in reader.fieldnames:
                    new_row['Image Alt Text'] = alt_text
                
                writer.writerow(new_row)

        update_stats(len(handle_order), added_count)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return jsonify({
            "csvContent": output.getvalue(),
            "fileName": f"augmented_catalog_{timestamp}.csv",
            "stats": {
                "totalProducts": len(handle_order),
                "added": added_count,
                "skipped": skipped_count,
                "totalRows": len(rows) + added_count
            },
            "global_stats": get_stats()
        })

    except Exception as e:
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

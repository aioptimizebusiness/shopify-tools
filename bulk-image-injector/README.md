# Shopify CSV Image Augmentor 🚀

A lightweight, local-first web utility for Shopify store owners to bulk-inject images (like certificates or brand badges) into their product catalogs.

## 🌟 Why use this?
Adding a single image (like a brand certificate or a "1-Year Warranty" badge) to 1,000+ products in Shopify usually requires a paid app or manual CSV editing. This tool automates the process:
- **Idempotent**: Won't add the same image twice if run multiple times.
- **In-Memory**: No data is stored on any server; processing happens entirely on your machine.
- **Shopify Compatible**: Preserves all 60+ standard Shopify CSV columns including metafields.

## 🛠️ Features
- **Dashboard UI**: Modern, glassmorphic interface for easy file uploads.
- **Bulk Analytics**: Instant feedback on processed vs. skipped products.
- **Encoding Support**: Handles UTF-8 with BOM (default Excel/Shopify export format).
- **Position Sensing**: Automatically places the new image as the *last* image in the product sequence.

## 🚀 How to Run Locally
1. **Clone the repo**:
   ```bash
   git clone https://github.com/yourusername/shopify-csv-augmentor.git
   cd shopify-csv-augmentor
   ```
2. **Install requirements**:
   ```bash
   pip install flask
   ```
3. **Run the app**:
   ```bash
   python app.py
   ```
4. **Access UI**: Open `http://127.0.0.1:5000` in your browser.

## 📄 License
This project is open-source under the **MIT License**. Feel free to use, modify, and distribute it!

## 🤝 Contributions
Contributions are welcome! If you have a feature request or bug report, please open an issue or submit a pull request.

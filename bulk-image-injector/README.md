# Bulk Image Injector 🖼️

A minimalist, high-performance utility for Shopify store owners to bulk-inject professional labels, certificates, warranty badges, and other images into their product catalog using a simple CSV export.

## 🚀 Live Demo
**[Use the Tool Online](https://apps.aioptimizebusiness.com/shopify/bulk-image-injector/)**

## ✨ Features
- **Idempotent processing**: Automatically detects if an image is already present to avoid duplicates.
- **Universal Injection**: Set a dynamic Image URL and Alt Text for any use case.
- **Shopify Compatible**: Correctly handles Shopify's CSV format, BOM, and image position logic.
- **Premium UI**: Minimalist dashboard with dark blue "Trust" branding and real-time usage statistics.
- **Privacy First**: Processes everything in-memory and returns the file directly; no data is stored permanently.

## 🛠️ Usage Instructions
1.  **Export Products**: From your Shopify Admin, export your products as a CSV.
2.  **Configuration**: Enter the URL of the image you want to add and specify its Alt text.
3.  **Upload**: Select or drag-and-drop your Shopify CSV file.
4.  **Process**: Click "Add Bulk Images".
5.  **Import**: Download the new CSV and import it back into Shopify. Select the option to **"Overwrite any current products that have the same handle."**

## 📦 Technical Setup (Local/Self-Hosted)
If you wish to run this tool on your own server:

### Prerequisites
- Python 3.8+
- Flask

### Installation
1.  Clone the repository:
    ```bash
    git clone https://github.com/aioptimizebusiness/shopify-tools.git
    cd bulk-image-injector
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    python app.py
    ```
4.  Access the app at `http://localhost:5000`.

### Docker Deployment
1.  Build the image:
    ```bash
    docker build -t shopify-image-injector .
    ```
2.  Run the container:
    ```bash
    docker run -p 5000:5000 shopify-image-injector
    ```

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🤝 Support
Created by **Yahya Bandukwala (AI Optimize Business)**.
- [Book a Strategy Audit](https://topmate.io/yahyab/1870347?utm_source=public_profile&utm_campaign=yahyab)
- [Main Website](https://aioptimizebusiness.com/)

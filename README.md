# Shopify Tools 🚀

A collection of free, open-source utility tools for Shopify store owners and developers. Designed to be lightweight, privacy-focused, and easy to deploy.

## ✨ Available Tools

### 1. [Bulk Image Injector](./bulk-image-injector)
Bulk inject professional labels, certificates, warranty badges, and other images into your Shopify product catalog using a simple CSV export.
- **Features**: Idempotent processing, SEO-friendly Alt text, automatic image positioning, and a premium dashboard UI.

---

## 🛠️ General Setup
Most tools in this repository are built with Python (Flask) and can be run locally or via Docker.

### Running Locally
1. Clone the repo:
   ```bash
   git clone https://github.com/aioptimizebusiness/shopify-tools.git
   ```
2. Navigate to the tool directory:
   ```bash
   cd bulk-image-injector
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python app.py
   ```

### Docker Deployment
Each tool directory contains a `Dockerfile`. To run via Docker:
```bash
docker build -t shopify-tool-name .
docker run -p 5000:5000 shopify-tool-name
```

## 📄 License
All tools in this repository are released under the **MIT License**.

## 🤝 Support & Contribution
Developed by **Yahya Bandukwala (AI Optimize Business)**. 
- [Main Website](https://aioptimizebusiness.com/)
- [Book a Strategy Audit](https://aioptimizebusiness.com/#contact)

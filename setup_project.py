"""
setup_project.py
────────────────
One-time setup for the Titanic Chat Agent:
  1. Installs all required Python packages
  2. Downloads the Titanic dataset from Kaggle and saves as titanic.csv
  3. Creates a .env file template if one doesn't exist

Run once before starting the backend:
    python setup_project.py
"""

import subprocess
import sys
import os

REQUIRED_PACKAGES = [
    "kagglehub[pandas-datasets]",
    "fastapi",
    "uvicorn",
    "pandas",
    "matplotlib",
    "langchain",
    "langchain-core",
    "langchain-community",
    "langchain-experimental",
    "langchain-classic",
    "huggingface_hub>=0.26.0",
    "transformers>=4.37.0",
    "python-dotenv",
    "streamlit>=1.27.0",
    "requests",
]

PROJECT_ROOT = os.path.dirname(__file__)
CSV_TARGET = os.path.join(PROJECT_ROOT, "titanic.csv")
ENV_FILE = os.path.join(PROJECT_ROOT, ".env")


def install_packages():
    print("\n📦 Installing packages...")
    for pkg in REQUIRED_PACKAGES:
        print(f"  → {pkg}")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", pkg]
        )
    print("✅ Packages installed.\n")


def download_titanic():
    if os.path.exists(CSV_TARGET):
        print(f"✅ titanic.csv already exists at {CSV_TARGET}, skipping download.\n")
        return

    print("📥 Downloading Titanic dataset from Kaggle...")
    try:
        from importlib import import_module
        kagglehub = import_module("kagglehub")
        from kagglehub import KaggleDatasetAdapter
    except Exception:
        print("⚠️ 'kagglehub' is not installed or could not be imported; attempting to install it now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "kagglehub[pandas-datasets]"])
        try:
            from importlib import import_module
            kagglehub = import_module("kagglehub")
            from kagglehub import KaggleDatasetAdapter
        except Exception as e:
            print("❌ Failed to import kagglehub after installation:", e)
            sys.exit(1)

    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "yasserh/titanic-dataset",
        "train.csv",
    )
    df.to_csv(CSV_TARGET, index=False)
    print(f"✅ Saved as {CSV_TARGET}  ({len(df)} rows)\n")


def create_env_template():
    if os.path.exists(ENV_FILE):
        print(f"✅ .env already exists, skipping.\n")
        return

    with open(ENV_FILE, "w") as f:
        f.write("# Get your token from https://huggingface.co/settings/tokens\n")
        f.write("HUGGINGFACEHUB_API_TOKEN=your_token_here\n")
    print(f"📝 Created .env template at {ENV_FILE}")
    print("   ⚠️  Edit it and add your HuggingFace token before running the server.\n")


def main():
    install_packages()
    download_titanic()
    create_env_template()
    print("🚀 Setup complete! Next steps:")
    print("   1. Add your HuggingFace token to .env")
    print("   2. Start backend:  uvicorn backend.main:app --host 0.0.0.0 --port 8000")
    print("   3. Start frontend: streamlit run frontend/app.py")


if __name__ == "__main__":
    main()
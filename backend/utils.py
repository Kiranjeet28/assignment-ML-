import io
import base64
import matplotlib.pyplot as plt
import pandas as pd

def detect_plot_needed(question: str) -> bool:
    """
    Simple heuristic to check if the user is asking for a visualization.
    """
    keywords = ["plot", "chart", "graph", "visualize", "histogram", "bar", "show me"]
    return any(kw in question.lower() for kw in keywords)

def generate_plot(df: pd.DataFrame, question: str) -> str | None:
    """
    Generates a plot based on keywords in the question and returns it as a base64 string.
    """
    try:
        plt.figure(figsize=(8, 5))
        q = question.lower()

        if "survived" in q or "survival" in q:
            df['Survived'].value_counts().plot(kind='bar', color=['red', 'green'])
            plt.title("Survival Count (0 = No, 1 = Yes)")
            plt.xlabel("Survived")
            plt.ylabel("Count")
        
        elif "class" in q or "pclass" in q:
            df['Pclass'].value_counts().sort_index().plot(kind='bar')
            plt.title("Passenger Class Distribution")
            plt.xlabel("Class")
            plt.ylabel("Count")

        elif "age" in q:
            df['Age'].dropna().hist(bins=20)
            plt.title("Age Distribution")
            plt.xlabel("Age")
            plt.ylabel("Frequency")

        elif "sex" in q or "gender" in q:
            df['Sex'].value_counts().plot(kind='pie', autopct='%1.1f%%')
            plt.title("Gender Distribution")
            plt.ylabel("")

        else:
            # Default fallback plot
            df.nunique().plot(kind='bar')
            plt.title("Unique Values per Column")

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')
    except Exception as e:
        print(f"Plotting error: {e}")
        return None

def log_user_query(question: str, answer: str):
    """
    Placeholder for logging logic (e.g., to a database or file).
    """
    print(f"LOG: Q: {question} | A: {answer[:50]}...")
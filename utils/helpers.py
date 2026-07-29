SAMPLE_TEXTS = {
    "RAG & Information Retrieval": (
        "Retrieval-Augmented Generation (RAG) is an AI framework for retrieving facts from an external "
        "knowledge base to ground large language models (LLMs) on the most accurate, up-to-date information. "
        "By doing so, it provides users with insight into the LLM's generative processes and reduces the risk "
        "of hallucinations.\n\n"
        "Grounding LLMs on external databases is crucial. Without RAG, an LLM takes a user query and generates "
        "a response based solely on the data it was trained on. This training data has a knowledge cutoff, meaning "
        "the LLM cannot answer questions about real-time events or proprietary private datasets.\n\n"
        "RAG solves this by introducing a retrieval step. When a query is received, the system queries a search index "
        "(often a vector database) to retrieve documents relevant to the query. These documents are then appended to "
        "the user prompt and sent to the LLM. The LLM synthesizes this retrieved context to construct its response, "
        "ensuring factual accuracy and source traceability."
    ),
    "The Story of the Golden Gate Bridge": (
        "The Golden Gate Bridge is a suspension bridge spanning the Golden Gate, the one-mile-wide strait connecting "
        "San Francisco Bay and the Pacific Ocean. The structure links the U.S. city of San Francisco, California—the "
        "northern tip of the San Francisco Peninsula—to Marin County, carrying both U.S. Route 101 and California State "
        "Route 1 across the strait.\n\n"
        "Designed by engineer Joseph Strauss in 1917, the bridge was initially declared impossible to build due to "
        "strong winds, thick fog, and deep waters. Despite these warnings, construction began in 1933. It was completed "
        "in 1937 at a cost of $35 million, ahead of schedule and $1.3 million under budget. At the time of its opening, "
        "it was both the longest and the tallest suspension bridge span in the world, with a main span of 4,200 feet "
        "and a total height of 746 feet.\n\n"
        "Today, the Golden Gate Bridge is an internationally recognized symbol of San Francisco and California. It has "
        "been declared one of the Wonders of the Modern World by the American Society of Civil Engineers. The bridge is "
        "famous for its International Orange color, chosen specifically to make it visible in San Francisco's frequent fog."
    ),
    "Technical Documentation Example": (
        "# Getting Started with PySpark\n\n"
        "PySpark is the Python API for Apache Spark, an open-source, distributed computing framework. "
        "It allows you to perform large-scale data processing in Python using Spark SQL, DataFrames, and MLlib.\n\n"
        "## Installation\n"
        "To install PySpark, make sure you have Python 3.8 or later and Java 8/11 installed. Run:\n"
        "```bash\n"
        "pip install pyspark\n"
        "```\n\n"
        "## Creating a SparkSession\n"
        "The entry point to programming Spark with the Dataset and DataFrame API is the SparkSession class. "
        "Here is how to initialize it:\n"
        "```python\n"
        "from pyspark.sql import SparkSession\n\n"
        "spark = SparkSession.builder \\\n"
        "    .appName('PySparkExample') \\\n"
        "    .getOrCreate()\n"
        "```\n\n"
        "## Loading Data\n"
        "You can load CSV, JSON, Parquet, and text files into a Spark DataFrame. For instance, loading a CSV file is done as follows:\n"
        "```python\n"
        "df = spark.read.csv('data.csv', header=True, inferSchema=True)\n"
        "df.show(5)\n"
        "```"
    )
}

def get_sample_text(key: str) -> str:
    return SAMPLE_TEXTS.get(key, "")

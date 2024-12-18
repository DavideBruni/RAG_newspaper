# RAG_newspaper 📰
RAG system with newspaper knoledge-base
# Knowledge Retrieval System with Metadata Filtering

This repository contains the implementation of a Retrieval-Augmented Generation (RAG) system. The system utilizes a knowledge base built from scraped articles from an online newspaper, leveraging metadata filtering to enhance retrieval and relevance. The core functionality includes scraping, chunking, indexing, and querying a vector database with a language model for interactive exploration and answering.

## Key Features

### 1. **Knowledge Base Construction** 🤓🔨
- **Scraping:** Articles are collected from a single online newspaper using the `scraper.py` script.
  - The script is executed daily via a `crontab` task to ensure the knowledge base remains up-to-date.
  - Access relies on the free availability of these articles.
- **Chunking:** During the indexing phase, articles are split into chunks based on their structure:
  - **Title**
  - **Summary**
  - **Paragraphs**
- **Metadata:** Additional metadata is extracted and stored alongside the content:
  - **Author**
  - **Publication Date**
  - **Section** (e.g., Politics, Foreign Affairs, Local News, etc.)

### 2. **Vector Database**
- The project uses **OpenSearch** as the vector store to index and retrieve document embeddings.
  - The OpenSearch index is configured with approximate k-Nearest Neighbor (k-NN) search enabled.
  - **Cosine similarity** is used as the metric for relevance.
  - Refer to the [OpenSearch documentation on approximate k-NN](https://opensearch.org/docs/latest/search-plugins/knn/approximate-knn/#:~:text=To%20use%20the%20k%2DNN,library%20indexes%20for%20the%20index.&text=In%20the%20preceding%20example%2C%20both,are%20configured%20using%20method%20definitions.) for details.

### 3. **Retrieval-Augmented Generation (RAG)**
- A RAG system is implemented to interactively query the knowledge base and retrieve relevant content.
  - The retrieval process leverages metadata filters for fine-tuned search results.
- The **Qwen-2.5** large language model (LLM) is used for text generation.
  - Note: The system is LLM-agnostic, allowing other models to be integrated if desired.
- A Jupyter Notebook is provided to:
  - Explore the creation of the RAG pipeline.
  - Execute end-to-end queries, returning generated outputs based on indexed content.
  - **Configuration:** The notebook requires setting environment-specific constants to function correctly.

### Notebook Execution
- Open the provided Jupyter Notebook to test the RAG pipeline.
- Adjust constants and configurations to match your local environment.
- Explore retrieval and response generation using the LLM.

## Future Improvements 🚀

1. **Expand Sources:**
   - Add support for scraping multiple online newspapers.
   - Include a metadata filter for the source.

2. **Enhance Prompt Engineering:**
   - Refine prompts for better-quality responses from the LLM.

3. **Text-to-Speech Integration:**
   - Pass generated outputs to a a better TTS system, allowing users to listen to the responses as if they were coming from a newscast.

## References and Tools Used ⚙️
- **LangChain:** Framework for building applications with LLMs ([LangChain GitHub](https://github.com/hwchase17/langchain)).
- **OpenSearch:** Vector database for indexing and approximate k-NN search ([OpenSearch Documentation](https://opensearch.org/docs/)).
- **Qwen-2.5:** Large language model for generation tasks ([Model Info](https://huggingface.co/Qwen)).
- **Multilingual-E5-Large:** Pretrained model for multilingual tasks ([Model Info](https://huggingface.co/intfloat/multilingual-e5-large)).

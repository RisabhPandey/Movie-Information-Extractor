# 🎬 CineScan --- Movie Information Extractor

> Turn an unstructured movie or TV-series description into clean,
> structured information with AI.

**Live Demo:** https://movie-information-extractor-01-22.streamlit.app

**GitHub Repository:** https://github.com/RisabhPandey/Movie-Information-Extractor

## Overview

CineScan is an AI-powered web application that extracts useful movie and
TV-series details from a paragraph of text. Paste a description,
synopsis, or article into the app and CineScan uses a language model to
organize the information into a validated structure.

The app presents the extracted information in a clean, card-based
interface and lets you inspect or download the result as JSON.

## ✨ Features

-   **AI-powered information extraction** from a movie or TV-series
    description.
-   **Structured output** for title, release year, genres, director,
    main cast, setting, plot, themes, rating, notable features, and a
    short summary.
-   **Schema validation** with Pydantic to keep the output in a
    predictable format.
-   **JSON export** so the extracted data can be reused in other
    applications.
-   **Sample descriptions** for trying the app quickly.
-   **Interactive Streamlit interface** with a custom dark theme and
    responsive layout.
-   **Error handling** for model-call failures and invalid structured
    responses.

## 🧰 Tech Stack

  Technology                  Purpose
  --------------------------- -------------------------------------------
  Python                      Application logic
  Streamlit                   Web interface
  Mistral AI                  Language model for extracting information
  LangChain                   Prompt construction and model integration
  Pydantic                    Data schema and validation
  `python-dotenv`             Loading local environment variables
  Git & GitHub                Version control and source hosting
  Streamlit Community Cloud   Web deployment

## ⚙️ How It Works

1.  Open the [live
    app](https://movie-information-extractor-01-22.streamlit.app/).
2.  Paste a paragraph describing a movie or TV series, or select one of
    the built-in samples.
3.  Click **Extract Information**.
4.  The app sends the text to Mistral AI through LangChain with
    instructions to return a JSON object.
5.  Pydantic parses and validates the response against the `Movie`
    schema.
6.  Review the extracted details, inspect the raw structured data, or
    download the result as a JSON file.

## 📋 Information Extracted

Depending on what is present in the supplied text, CineScan can extract:

-   Title
-   Release year
-   Genre
-   Director
-   Main cast
-   Setting/location
-   Plot
-   Themes
-   Rating
-   Notable features
-   Short summary

The model is instructed to use `null` for information that is not
mentioned. Results depend on the quality and completeness of the input
and should be reviewed when accuracy is important.

## 🖥️ Run Locally

### 1. Clone the repository

``` bash
git clone https://github.com/RisabhPandey/Movie-Information-Extractor.git
cd Movie-Information-Extractor
```

> The repository may contain more than one project folder. Run the
> following commands from the directory that contains `UICore.py` and
> `requirements.txt`. If those files are inside `RiyourSA`, first run
> `cd RiyourSA`.

### 2. Create and activate a virtual environment (recommended)

**Windows PowerShell**

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure your Mistral API key

Create a `.env` file in the project directory:

``` env
MISTRAL_API_KEY=your_mistral_api_key_here
```

Get an API key from the [Mistral AI
platform](https://console.mistral.ai/).

**Security:** Never commit your `.env` file or publish your API key.
Keep `.env` in `.gitignore`. For Streamlit Community Cloud, configure
`MISTRAL_API_KEY` in the app's **Settings → Secrets** instead of
uploading a `.env` file.

### 5. Start the app

``` bash
streamlit run UICore.py
```

Streamlit will print a local URL in the terminal, usually
`http://localhost:8501`.

## 🔐 Configuration

The app expects the `MISTRAL_API_KEY` environment variable to be
available. Locally, it is loaded with `python-dotenv`; in deployment,
set it through the hosting provider's secret-management settings.

If the app reports `ModuleNotFoundError: No module named 'dotenv'`,
verify that `python-dotenv` is listed in `requirements.txt` and that the
deployment has completed a fresh dependency installation.

## 📁 Project Structure

The main files include:

``` text
.
├── UICore.py          # Streamlit UI and application flow
├── core.py            # Supporting project logic
├── structured.py      # Supporting structured-data logic
├── requirements.txt   # Python dependencies
├── .gitignore         # Files excluded from version control
└── README.md          # Project documentation
```

The exact responsibilities of `core.py` and `structured.py` depend on
the current implementation in those files.

## 🧪 Example

**Input**

> Interstellar (2014) is a science-fiction film directed by Christopher
> Nolan. It follows a team of astronauts searching for a new home for
> humanity. The film explores love, time, and survival.

**Possible structured output** (illustrative):

``` json
{
  "title": "Interstellar",
  "release_year": 2014,
  "genre": ["Science fiction"],
  "director": "Christopher Nolan",
  "main_cast": null,
  "setting_location": null,
  "plot": "A team of astronauts searches for a new home for humanity.",
  "themes": ["Love", "Time", "Survival"],
  "ratings": null,
  "notable_features": null,
  "short_summary": null
}
```

The actual output depends on the supplied text and the model response.

## ⚠️ Limitations

-   CineScan extracts information from the text you provide; it is not a
    movie database search engine.
-   Information that is absent from the input may be returned as `null`.
-   AI-generated extraction can be incomplete or incorrect. Verify
    important details independently.
-   The app requires a valid Mistral API key and access to the
    configured model.

## 🚀 Future Improvements

Potential improvements include batch extraction, richer validation and
retry handling, extraction confidence indicators, support for additional
input formats, and automated tests.

## 🤝 Contributing

Suggestions and improvements are welcome. You can open an issue or
submit a pull request through the [GitHub
repository](https://github.com/RisabhPandey/Movie-Information-Extractor).

## 📄 License

No license has been specified here. Unless a license is added to the
repository, reuse and redistribution are not automatically granted. Add
a `LICENSE` file if you want to publish explicit reuse terms.

------------------------------------------------------------------------

Made with Python, Streamlit, LangChain, Mistral AI, and Pydantic. 🎬

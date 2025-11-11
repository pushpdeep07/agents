# Deep Agents with LangGraph & LangChain

> A hands-on code-along for building advanced, multi-step agents using LangChain and LangGraph.

This project is a Python application that serves as the codebase for the [LangChain Academy course on Deep Agents](https://academy.langchain.com/courses/deep-agents-with-langgraph). It implements a series of "deep agents"—advanced agents that can plan, use tools, manage files, and delegate tasks to sub-agents.

---

## 🚀 Features

* **Progressive Learning:** Organized into a series of Jupyter Notebooks (`0_...` to `4_...`) that gradually build in complexity.
* **LangGraph Integration:** Uses LangGraph to build stateful, robust, and cyclical agent workflows, moving beyond simple agent loops.
* **Advanced Agent Skills:** Implements practical, complex features like:
    * Task planning (maintaining a TODO list).
    * A virtual file system (using `ls`, `read_file`, `write_file`).
    * Sub-agent delegation (passing tasks to specialized agents).
* **Configurable:** Loads all API keys and configurations from a standard `.env` file for security and flexibility.
* **Practical Tool Use:** Demonstrates how to give agents tools for real-world tasks, like web searches using the Tavily API.

---

## 🛠️ Getting Started

Follow these instructions to get the project and all its dependencies running on your local machine.

### Prerequisites

You will need the following tools installed on your computer:
* [Python 3.10+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads/)

### Installation

1.  **Clone the repo**
    ```bash
    git clone [https://github.com/pushpdeep07/agents.git](https://github.com/pushpdeep07/agents.git)
    cd agents
    ```
2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```
3.  **Install dependencies**
    ```bash
    pip install langchain langgraph langchain-openai tavily-python python-dotenv jupyter
    ```
    *(**Note:** This command installs all the necessary libraries for LangChain, LangGraph, OpenAI models, Tavily search, environment files, and running the Jupyter notebooks.)*

4.  **Set up environment variables**
    Create a file named `.env` in the root directory and add your API keys. You will need an OpenAI key and a Tavily search key for the notebooks to work.
    ```ini
    # Service API Keys
    OPENAI_API_KEY="sk-..."
    TAVILY_API_KEY="tvly-..."
    
    # Optional, if you want to use Anthropic models
    ANTHROPIC_API_KEY="sk-ant-..."
    ```

---

## 🏃‍♀️ Usage & Steps to Test

This project is a series of tutorials. The "tests" are the agent runs within each notebook.

1.  **Start the Jupyter Server**
    From your terminal (with your `venv` activated), run:
    ```bash
    jupyter lab
    ```
    This will open a new tab in your browser with the JupyterLab interface.

2.  **Open the First Notebook**
    On the left-hand file explorer in Jupyter, double-click `0_create_agent.ipynb` to open it.

3.  **Run the Setup Cells**
    Click on the first code cell (which starts with `import ...`) and press **Shift+Enter** to run it. Continue running the next few cells to import dependencies and load your API keys from the `.env` file.

4.  **Define the Agent**
    Run the cells that define the tools, the LLM, and the agent itself. You will see a cell that defines `agent_executor = ...`.

5.  **Run the Test**
    Find the cell that contains the `.invoke()` command, which looks something like this:
    ```python
    # This is the test!
    response = agent_executor.invoke({
        "messages": [("user", "What's the weather in San Francisco?")]
    })
    
    print(response['messages'][-1].content)
    ```
    Run this cell by pressing **Shift+Enter**.

6.  **Verify the Output**
    Watch the output of the cell. You are "passing the test" if:
    * The agent shows its "thought" process.
    * It correctly identifies and uses a tool (like `tavily_search`).
    * It provides a correct, final answer to the question.

7.  **Experiment!**
    The best way to test is to **change the user input**. In the `.invoke()` cell, try asking your own questions to see how the agent responds.
    ```python
    # Change this line to your own question:
    "messages": [("user", "Who won the last F1 race?")]
    ```

8.  **Continue to the Next Notebook**
    Once you understand the first notebook, close it and open `1_todo.ipynb` to learn the next concept. Repeat the process of running cells and experimenting with the inputs.

# AI_Nagotiation# AI_Nagotiation

## Overview

**AI_Nagotiation** is a Python project that simulates automated negotiations between buyer and seller agents. The main focus is on developing and testing a hyper-adaptive buyer agent that uses strategic, data-driven negotiation tactics to maximize savings and ensure successful deals.

## Features

- **Custom Negotiation Agents:**  
  Includes a highly adaptive buyer agent (`YourBuyerAgent`) with analytical and pragmatic negotiation logic.
- **Test Harness:**  
  Simulate negotiations with different products, budgets, and seller personalities using the provided test runner.
- **Mock Seller Agent:**  
  A configurable seller agent for robust and repeatable testing.
- **Extensible Design:**  
  Modular code structure for easy addition of new agent types or negotiation scenarios.

## How It Works

1. **Define Products:**  
   Products are described with attributes like name, category, quantity, quality, origin, and market price.

2. **Run Negotiations:**  
   Buyer and seller agents exchange offers and messages over several rounds, aiming to reach a mutually acceptable deal.

3. **Evaluate Performance:**  
   The test runner reports on deal success, savings, and negotiation efficiency.

## Getting Started

1. **Install dependencies:**  
   (If you use any external libraries, list them in `requirements.txt`.)

2. **Run the test script:**  
   ```
   python testing_gem.py
   ```

3. **(Optional) Integrate with Ollama LLM:**  
   You can enhance your agent with LLM-powered negotiation by connecting to [Ollama](https://ollama.com/).

## File Structure

- `negotiation_agent_gem.py` — Core agent classes and negotiation logic.
- `testing_gem.py` — Test runner and mock seller for evaluating agent performance.
- `README.md` — Project documentation.

## Customization

You can create your own negotiation agent by subclassing `BaseBuyerAgent` and implementing your own strategy.




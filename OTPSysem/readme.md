#  Secure OTP Verification Demo

A lightweight Python and Flask application demonstrating secure **One-Time Password (OTP)** generation, rate limiting, and verification principles to prevent common web security vulnerabilities.

##  Key Security Features

* **Cryptographic Randomness:** Uses Python's `secrets` module (rather than `random`) for generating unpredictable 6-digit OTP codes.

* **Rate Limiting:** Prevents spam and resource exhaustion by enforcing a **60-second cooldown** between OTP requests for the same email.

* **Expiration & Attempt Controls:**

  * OTPs automatically expire after **5 minutes** ($300\text{ seconds}$).

  * Restricts verification to a maximum of **5 failed attempts** to prevent brute-force attacks.

* **Timing-Safe Comparison:** Uses `hmac.compare_digest` during OTP verification to prevent side-channel timing attacks.

## Repository Structure

```
├── app.py              # Main Flask application and verification logic
├── requirements.txt    # Application dependencies
└── README.md           # Project documentation

```

##  Setup & Installation

### 1. Prerequisites

Ensure you have **Python 3.8+** installed on your system.

### 2. Virtual Environment Setup

Create and activate a virtual environment on your local machine:

**Windows (Command Prompt / PowerShell):**

```
python -m venv venv
venv\Scripts\activate

```

**macOS / Linux:**

```
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

Install the required packages from `requirements.txt`:

```
pip install -r requirements.txt

```

### 4. Running the Application

Execute the Flask application:

```
python app.py

```

Navigate to **`http://127.0.0.1:5000`** in your web browser.

>  **Note:** Since this is a learning demonstration, generated OTP codes are printed directly to your VS Code / terminal console instead of sending real emails.

##  Educational Disclaimer

*This repository is created for learning, testing security concepts, and educational analysis purposes only.*
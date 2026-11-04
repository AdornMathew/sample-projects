
from flask import Flask, request, render_template_string
import secrets
import time
import hmac

app = Flask(__name__)

# Temporary storage for this learning demonstration.
otp_store = {}

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>OTP Verification</title>
</head>
<body>
    <h2>Request an OTP</h2>

    <form action="/request-otp" method="POST">
        <input type="email" name="email"
               placeholder="Enter your email" required>
        <button type="submit">Send OTP</button>
    </form>

    <hr>

    <h2>Verify OTP</h2>

    <form action="/verify" method="POST">
        <input type="email" name="email"
               placeholder="Enter your email" required>
        <input type="text" name="otp"
               placeholder="Six-digit OTP"
               pattern="[0-9]{6}" maxlength="6" required>
        <button type="submit">Verify</button>
    </form>

    <p>{{ message }}</p>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(PAGE, message="")


@app.route("/request-otp", methods=["POST"])
def request_otp():
    email = request.form.get("email", "").strip().lower()

    if not email or len(email) > 254:
        return render_template_string(
            PAGE, message="Enter a valid email address."
        ), 400

    # Limit how often a new OTP can be requested.
    previous = otp_store.get(email)
    now = time.time()

    if previous and now - previous["created"] < 60:
        return render_template_string(
            PAGE, message="Please wait before requesting another OTP."
        ), 429

    code = f"{secrets.randbelow(1_000_000):06d}"

    otp_store[email] = {
        "code": code,
        "created": now,
        "expires": now + 300,
        "attempts": 0,
    }

    # Demonstration only: do not log OTPs in production.
    print(f"Demo OTP for {email}: {code}")

    return render_template_string(
        PAGE, message="Demo OTP generated. Check the VS Code terminal."
    )


@app.route("/verify", methods=["POST"])
def verify():
    email = request.form.get("email", "").strip().lower()
    submitted = request.form.get("otp", "")

    record = otp_store.get(email)

    if not record:
        return render_template_string(
            PAGE, message="No active OTP. Request a new one."
        )

    if time.time() >= record["expires"]:
        del otp_store[email]
        return render_template_string(
            PAGE, message="OTP expired. Request a new one."
        )

    if record["attempts"] >= 5:
        del otp_store[email]
        return render_template_string(
            PAGE, message="Too many attempts. Request a new OTP."
        )

    record["attempts"] += 1

    if not (
        len(submitted) == 6
        and submitted.isascii()
        and submitted.isdigit()
        and hmac.compare_digest(record["code"], submitted)
    ):
        return render_template_string(
            PAGE, message="Incorrect OTP."
        )

    del otp_store[email]

    return render_template_string(
        PAGE, message="OTP verified successfully!"
    )


if __name__ == "__main__":
    app.run(debug=True)

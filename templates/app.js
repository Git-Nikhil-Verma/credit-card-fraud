async function processInput() {
    const rawInput = document.getElementById('inputValues').value.trim();

    // Remove any extra spaces between values and split by space
    const inputArray = rawInput.split(/\s+/).map(value => parseFloat(value.trim()));

    console.log('Input Array:', inputArray);
    console.log('Input Length:', inputArray.length);

    // Validate input: There should be exactly 30 numeric values
    if (inputArray.length !== 30 || inputArray.some(isNaN)) {
        document.getElementById('result').innerText =
            '❌ Please enter exactly 30 numeric values separated by spaces in the format: Time V1 V2 ... V28 Amount.';
        return;
    }

    // Create the dictionary
    const formData = {};
    formData['Time'] = inputArray[0];
    for (let i = 1; i <= 28; i++) {
        formData[`V${i}`] = inputArray[i];
    }
    formData['Amount'] = inputArray[29];

    try {
        // Send data to backend API (adjust URL as needed)
        const response = await fetch('http://192.168.x.x:5000/predict', { // Adjust URL here if deployed
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();

        // Display the prediction result
        document.getElementById('result').innerText =
            result.prediction === 1
                ? '🚨 Fraudulent Transaction Detected!'
                : '✅ Legitimate Transaction.';
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').innerText =
            '❌ Error predicting fraud. Please check your backend server connection.';
    }
}

function copyExample(exampleId) {
    const exampleText = document.getElementById(exampleId).textContent.trim();
    navigator.clipboard.writeText(exampleText).then(() => {
        displayCopyMessage(`Message copied to clipboard!`);
    }).catch(err => {
        console.error('Error copying text: ', err);
        displayCopyMessage('❌ Failed to copy message!');
    });
}

function displayCopyMessage(message) {
    const messageContainer = document.getElementById('copyMessage');
    messageContainer.textContent = message; // Update the message container
    messageContainer.style.display = 'block'; // Ensure it is visible

    // Clear the message after 3 seconds
    setTimeout(() => {
        messageContainer.style.display = 'none';
    }, 2000);
}

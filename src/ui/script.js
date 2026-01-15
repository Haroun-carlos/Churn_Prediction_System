document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const btn = document.getElementById('predictBtn');
    const resultSection = document.getElementById('resultSection');
    const predictionResult = document.getElementById('predictionResult');
    const probIndicator = document.getElementById('probIndicator');
    const probValue = document.getElementById('probValue');
    
    // UI Feedback
    btn.disabled = true;
    btn.textContent = 'Analyzing...';
    
    // Gather form data
    const formData = new FormData(e.target);
    const data = {};
    formData.forEach((value, key) => {
        // Convert numeric fields
        if (['tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen'].includes(key)) {
            data[key] = parseFloat(value);
        } else {
            data[key] = value;
        }
    });
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        
        if (!response.ok) throw new Error('Prediction failed');
        
        const result = await response.json();
        
        // Update UI with results
        resultSection.classList.remove('hidden');
        predictionResult.textContent = result.prediction;
        
        if (result.prediction === 'Churn') {
            predictionResult.className = 'churn-yes';
            probIndicator.style.background = '#ef4444';
        } else {
            predictionResult.className = 'churn-no';
            probIndicator.style.background = '#22c55e';
        }
        
        const probPercentage = (result.probability * 100).toFixed(1);
        probValue.textContent = `${probPercentage}%`;
        
        // Animate progress bar
        setTimeout(() => {
            probIndicator.style.width = `${probPercentage}%`;
        }, 100);
        
        // Scroll to results
        resultSection.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to connect to the prediction server. Please ensure the backend is running.');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Analyze Churn Risk';
    }
});

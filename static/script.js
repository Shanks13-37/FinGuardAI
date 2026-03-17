document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('transaction-form');
    if (!form) return; // Only execute on the user dashboard page

    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');
    const resultPanel = document.getElementById('result-panel');

    // Result Elements
    const statusBadge = document.getElementById('tx-status-badge');
    const probBar = document.getElementById('prob-bar');
    const probValue = document.getElementById('prob-value');
    const llmMessage = document.getElementById('llm-message');
    const shapList = document.getElementById('shap-list');
    const txActions = document.getElementById('tx-actions');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // UI State: Loading
        submitBtn.disabled = true;
        btnText.textContent = 'Processing...';
        loader.classList.remove('hidden');
        resultPanel.classList.remove('hidden');

        // Reset old results visually
        probBar.style.width = '0%';
        probBar.style.backgroundColor = 'var(--text-muted)';
        statusBadge.textContent = 'Analyzing...';
        statusBadge.className = 'status-badge';
        llmMessage.textContent = 'Generating contextual analysis via GPT...';
        shapList.innerHTML = '';
        txActions.classList.add('hidden');

        // Capture data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/api/transaction', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (!response.ok) throw new Error('API request failed');

            const result = await response.json();

            // Artificial delay for effect (Simulating complex ML + LLM latency)
            setTimeout(() => {
                updateUIWithResults(result.prediction, result.explanation);

                // UI State: Reset Button
                submitBtn.disabled = false;
                btnText.textContent = 'Send Payment';
                loader.classList.add('hidden');
            }, 1500);

        } catch (error) {
            console.error('Error:', error);
            statusBadge.textContent = 'Error';
            statusBadge.className = 'status-badge danger';
            llmMessage.textContent = 'A system error occurred while processing your transaction.';

            submitBtn.disabled = false;
            btnText.textContent = 'Retry Payment';
            loader.classList.add('hidden');
        }
    });

    function updateUIWithResults(prediction, explanation) {
        const prob = prediction.probability;
        const isFraud = prediction.is_fraud;

        // Animate progress bar
        probBar.style.width = `${prob}%`;

        // Count up animation for text
        let start = 0;
        const duration = 1000;
        const stepTime = Math.abs(Math.floor(duration / prob));

        const countInt = setInterval(() => {
            start += 1;
            probValue.textContent = start;
            if (start >= Math.floor(prob)) clearInterval(countInt);
        }, stepTime);

        // Styling based on risk level
        if (isFraud || prob >= 65) {
            probBar.style.backgroundColor = 'var(--danger)';
            llmMessage.style.borderLeftColor = 'var(--danger)';
            statusBadge.textContent = 'Fraud Alert';
            statusBadge.className = 'status-badge danger';
            txActions.classList.remove('hidden'); // Show cancel/proceed options for high risk
        } else if (prob >= 30) {
            probBar.style.backgroundColor = 'var(--warning)';
            llmMessage.style.borderLeftColor = 'var(--warning)';
            statusBadge.textContent = 'Review Required';
            statusBadge.className = 'status-badge warning';
            txActions.classList.remove('hidden'); // Optional warning actions
        } else {
            probBar.style.backgroundColor = 'var(--success)';
            llmMessage.style.borderLeftColor = 'var(--success)';
            statusBadge.textContent = 'Verified';
            statusBadge.className = 'status-badge success';
        }

        // Update Context LLM text
        llmMessage.textContent = explanation;

        // Populate SHAP values
        prediction.shap_values.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span>${item.feature}</span>
                <div class="shap-value-bar">
                    <div class="shap-value-fill" style="width: ${item.importance}%"></div>
                </div>
                <span>${item.importance}%</span>
            `;
            shapList.appendChild(li);
        });
    }

    // Handlers for action buttons (Mocking behavior)
    if (document.getElementById('cancel-btn')) {
        document.getElementById('cancel-btn').addEventListener('click', () => {
            alert('Transaction successfully cancelled.');
            location.reload();
        });
    }

    if (document.getElementById('proceed-btn')) {
        document.getElementById('proceed-btn').addEventListener('click', () => {
            if (confirm('Are you strictly sure you want to proceed despite the fraud warning?')) {
                alert('Transaction pushed through manual override review queue.');
                location.reload();
            }
        });
    }
});

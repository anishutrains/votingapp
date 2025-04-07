// Global variables
let voteChart = null;
let currentVoterId = null;

// DOM elements
const registrationForm = document.getElementById('registration-form');
const voterForm = document.getElementById('voter-form');
const candidatesSection = document.getElementById('candidates-section');
const candidatesContainer = document.getElementById('candidates-container');
const statisticsSection = document.getElementById('statistics-section');

// Modal elements
const modal = document.getElementById('popup-modal');
const modalMessage = document.getElementById('modal-message');
const modalButton = document.getElementById('modal-button');
const closeModal = document.querySelector('.close-modal');

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    loadCandidates();
    loadStatistics();
    
    // Registration form submission
    voterForm.addEventListener('submit', handleRegistration);
    
    // Modal close button
    closeModal.addEventListener('click', closePopupModal);
    
    // Modal OK button
    modalButton.addEventListener('click', closePopupModal);
    
    // Close modal when clicking outside
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            closePopupModal();
        }
    });
});

// Handle voter registration
async function handleRegistration(event) {
    event.preventDefault();
    
    const voterName = document.getElementById('voter-name').value.trim();
    
    if (!voterName) {
        showPopup('Please enter your name');
        return;
    }
    
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: voterName })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentVoterId = data.voter_id;
            showPopup('Registration successful! You can now vote.', 'success');
            registrationForm.classList.add('hidden');
            candidatesSection.classList.remove('hidden');
            loadCandidates();
        } else {
            showPopup(data.message || 'Registration failed');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showPopup('Registration failed. Please try again.');
    }
}

// Load candidates from the server
async function loadCandidates() {
    try {
        const response = await fetch('/api/candidates');
        const data = await response.json();
        
        if (data.success) {
            displayCandidates(data.candidates);
        } else {
            showPopup('Failed to load candidates');
        }
    } catch (error) {
        console.error('Error loading candidates:', error);
        showPopup('Failed to load candidates');
    }
}

// Display candidates in the UI
function displayCandidates(candidates) {
    candidatesContainer.innerHTML = '';
    
    candidates.forEach(candidate => {
        const card = document.createElement('div');
        card.className = 'candidate-card';
        
        // Determine party color
        const partyColor = candidate.party.toLowerCase().includes('democratic') ? '#3498db' : '#e74c3c';
        
        card.innerHTML = `
            <img src="${candidate.image_url}" alt="${candidate.name}" class="candidate-image">
            <div class="candidate-info">
                <h3 class="candidate-name">${candidate.name}</h3>
                <p class="candidate-party" style="color: ${partyColor}">${candidate.party}</p>
                <button class="vote-button" onclick="voteForCandidate(${candidate.id})">
                    <i class="fas fa-vote-yea"></i> Vote for ${candidate.name}
                </button>
            </div>
        `;
        
        candidatesContainer.appendChild(card);
    });
}

// Vote for a candidate
async function voteForCandidate(candidateId) {
    try {
        const response = await fetch('/api/vote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ candidate_id: candidateId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showPopup('Vote recorded successfully! Thank you for participating in democracy.', 'success');
            loadStatistics();
            candidatesSection.classList.add('hidden');
        } else {
            showPopup(data.message || 'Voting failed');
        }
    } catch (error) {
        console.error('Voting error:', error);
        showPopup('Voting failed. Please try again.');
    }
}

// Load statistics from the server
async function loadStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const data = await response.json();
        
        if (data.success) {
            updateChart(data.statistics);
        } else {
            showPopup('Failed to load statistics');
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
        showPopup('Failed to load statistics');
    }
}

// Update the chart with new statistics
function updateChart(statistics) {
    const ctx = document.getElementById('voteChart').getContext('2d');
    
    if (voteChart) {
        voteChart.destroy();
    }
    
    // Determine colors based on party
    const colors = statistics.map(stat => {
        if (stat.name.includes('Biden')) return '#3498db'; // Democratic blue
        if (stat.name.includes('Trump')) return '#e74c3c'; // Republican red
        return '#95a5a6'; // Default gray
    });
    
    voteChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: statistics.map(stat => stat.name),
            datasets: [{
                data: statistics.map(stat => stat.votes),
                backgroundColor: colors,
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            size: 14,
                            weight: 'bold'
                        },
                        padding: 20
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
                            return `${label}: ${value} votes (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Show popup modal instead of alert
function showPopup(message, type = 'info') {
    modalMessage.textContent = message;
    
    // Set color based on message type
    if (type === 'success') {
        modalMessage.style.color = 'var(--success-color)';
    } else if (type === 'error') {
        modalMessage.style.color = 'var(--error-color)';
    } else {
        modalMessage.style.color = 'var(--dark-color)';
    }
    
    // Show the modal
    modal.style.display = 'flex';
}

// Close the popup modal
function closePopupModal() {
    modal.style.display = 'none';
} 
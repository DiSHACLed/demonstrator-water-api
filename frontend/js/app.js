// Configuration
const API_BASE_URL = 'https://dishacled-api.azurewebsites.net/api/v1';

// State
let autoRefreshInterval = null;

// DOM Elements
const waterLevelSlider = document.getElementById('waterLevel');
const levelValueDisplay = document.getElementById('levelValue');
const applyBtn = document.getElementById('applyBtn');
const resetBtn = document.getElementById('resetBtn');
const autoRefreshCheckbox = document.getElementById('autoRefresh');
const refreshBtn = document.getElementById('refreshBtn');
const activeSourceRadios = document.getElementsByName('activeSource');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    fetchActiveSource();
    fetchCurrentSettings(); // Restore slider to last-set value
    fetchAllData();
    setupAutoRefresh();
});

// Event Listeners
function setupEventListeners() {
    // Slider value display update
    waterLevelSlider.addEventListener('input', (e) => {
        levelValueDisplay.textContent = e.target.value;
    });

    // Apply settings button
    applyBtn.addEventListener('click', applySettings);

    // Reset button
    resetBtn.addEventListener('click', resetSettings);

    // Manual refresh button
    refreshBtn.addEventListener('click', fetchAllData);

    // Auto-refresh toggle
    autoRefreshCheckbox.addEventListener('change', (e) => {
        if (e.target.checked) {
            setupAutoRefresh();
        } else {
            clearAutoRefresh();
        }
    });

    // Active source radio buttons
    activeSourceRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.checked) {
                setActiveSource(e.target.value);
            }
        });
    });
}

// API Functions
async function applySettings() {
    const level = parseFloat(waterLevelSlider.value);

    try {
        const response = await fetch(`${API_BASE_URL}/control/set-level`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                level_percentage: level
            })
        });

        if (!response.ok) {
            throw new Error('Failed to apply settings');
        }

        const result = await response.json();
        console.log('Settings applied:', result);

        // Visual feedback
        applyBtn.textContent = '✓ Applied!';
        applyBtn.style.background = '#10b981';
        
        setTimeout(() => {
            applyBtn.textContent = 'Apply Settings';
            applyBtn.style.background = '';
        }, 2000);

        // Wait a moment for backend to update, then fetch new data
        await new Promise(resolve => setTimeout(resolve, 200));
        fetchAllData();

    } catch (error) {
        console.error('Error applying settings:', error);
        applyBtn.textContent = '✗ Error';
        applyBtn.style.background = '#ef4444';
        
        setTimeout(() => {
            applyBtn.textContent = 'Apply Settings';
            applyBtn.style.background = '';
        }, 2000);
    }
}

async function resetSettings() {
    waterLevelSlider.value = 30;
    levelValueDisplay.textContent = '30';
    
    await applySettings();
}

async function setActiveSource(sourceName) {
    try {
        const response = await fetch(`${API_BASE_URL}/control/set-active-source`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                source_name: sourceName
            })
        });

        if (!response.ok) {
            throw new Error('Failed to set active source');
        }

        const result = await response.json();
        console.log('Active source changed:', result);

        // Wait a moment for backend to propagate the change, then refresh data
        await new Promise(resolve => setTimeout(resolve, 300));
        await fetchAllData();

    } catch (error) {
        console.error('Error setting active source:', error);
    }
}

async function fetchActiveSource() {
    try {
        const response = await fetch(`${API_BASE_URL}/control/active-source`, {
            cache: 'no-store',
            headers: {
                'Cache-Control': 'no-cache'
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch active source');
        }

        const data = await response.json();
        const activeSource = data.value;
        
        // Update radio button to match backend state
        activeSourceRadios.forEach(radio => {
            radio.checked = radio.value === activeSource;
        });

    } catch (error) {
        console.error('Error fetching active source:', error);
    }
}

async function fetchCurrentSettings() {
    try {
        const response = await fetch(`${API_BASE_URL}/control/current-settings`, {
            cache: 'no-store',
            headers: {
                'Cache-Control': 'no-cache'
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch current settings');
        }

        const data = await response.json();
        const levelPercentage = data.value;
        
        // Update slider and display to match backend state
        waterLevelSlider.value = levelPercentage;
        levelValueDisplay.textContent = levelPercentage;

    } catch (error) {
        console.error('Error fetching current settings:', error);
    }
}

async function fetchSourceData(source) {
    try {
        const response = await fetch(`${API_BASE_URL}/${source}/current`, {
            cache: 'no-store',
            headers: {
                'Cache-Control': 'no-cache'
            }
        });
        
        if (!response.ok) {
            throw new Error(`Failed to fetch ${source} data`);
        }

        const data = await response.json();
        updateSourceDisplay(source, data);
        
    } catch (error) {
        console.error(`Error fetching ${source}:`, error);
        updateSourceError(source);
    }
}

async function fetchAllData() {
    await Promise.all([
        fetchSourceData('source-a'),
        fetchSourceData('source-b')
    ]);
}

// UI Update Functions
function updateSourceDisplay(source, data) {
    const sourceId = source === 'source-a' ? 'A' : 'B';
    const valueElement = document.getElementById(`source${sourceId}Value`);
    const timeElement = document.getElementById(`source${sourceId}Time`);
    const statusElement = document.getElementById(`source${sourceId}Status`);

    // Update value
    valueElement.textContent = data.value.toFixed(2);

    // Update timestamp
    const timestamp = new Date(data.measuredAt);
    timeElement.textContent = `Updated: ${timestamp.toLocaleTimeString()}`;

    // Update status
    statusElement.className = 'reading-status';
    statusElement.innerHTML = '<span class="status-dot"></span>';

    // Add warning for high values (above 80% threshold)
    const isHighLevel = (source === 'source-a' && data.value > 2020) || 
                        (source === 'source-b' && data.value > 20200);
    
    if (isHighLevel) {
        statusElement.innerHTML += ' ⚠️ High Water Level!';
        statusElement.style.fontWeight = 'bold';
    }

    // Update threshold highlighting (only for Source A in cm)
    if (source === 'source-a') {
        updateThresholdHighlighting(data.value);
    }
}

function updateThresholdHighlighting(valueCm) {
    // Convert cm to meters for comparison
    const valueMeters = valueCm / 100;
    
    // Define thresholds in meters
    const thresholds = [
        { max: 18.20, className: 'threshold-safe' },
        { max: 19.30, className: 'threshold-normal' },
        { max: 20.00, className: 'threshold-warning' },
        { max: 21.35, className: 'threshold-danger' },
        { max: Infinity, className: 'threshold-critical' }
    ];
    
    // Remove all active states
    document.querySelectorAll('.threshold-row').forEach(row => {
        row.classList.remove('threshold-active');
    });
    
    // Find and highlight the current threshold
    for (let i = 0; i < thresholds.length; i++) {
        if (valueMeters <= thresholds[i].max) {
            const rows = document.querySelectorAll(`.${thresholds[i].className}`);
            rows.forEach(row => row.classList.add('threshold-active'));
            break;
        }
    }
}

function updateSourceError(source) {
    const sourceId = source === 'source-a' ? 'A' : 'B';
    const valueElement = document.getElementById(`source${sourceId}Value`);
    const statusElement = document.getElementById(`source${sourceId}Status`);

    valueElement.textContent = '--';
    statusElement.className = 'reading-status error';
    statusElement.innerHTML = '<span class="status-dot"></span> Connection Error';
}

// Auto-refresh Functions
function setupAutoRefresh() {
    clearAutoRefresh();
    autoRefreshInterval = setInterval(fetchAllData, 5000); // Refresh every 5 seconds
}

function clearAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
    }
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    clearAutoRefresh();
});

// Export for debugging
window.dishacled = {
    fetchAllData,
    applySettings,
    resetSettings,
    API_BASE_URL
};

console.log('DiSHACLed Control Center initialized 💧');
console.log('API Base URL:', API_BASE_URL);
console.log('Debug functions available at window.dishacled');

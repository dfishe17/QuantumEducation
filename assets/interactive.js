// Interactive features initialization
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializeLearnMoreButtons();
});

function initializeTooltips() {
    const tooltips = document.querySelectorAll('.tooltip');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseover', function() {
            const tooltipText = this.querySelector('.tooltiptext');
            if (tooltipText) {
                tooltipText.style.visibility = 'visible';
                tooltipText.style.opacity = '1';
            }
        });

        tooltip.addEventListener('mouseout', function() {
            const tooltipText = this.querySelector('.tooltiptext');
            if (tooltipText) {
                tooltipText.style.visibility = 'hidden';
                tooltipText.style.opacity = '0';
            }
        });
    });
}

function initializeLearnMoreButtons() {
    const learnMoreButtons = document.querySelectorAll('[id^="learn_more_"]');
    learnMoreButtons.forEach(button => {
        button.addEventListener('click', function() {
            const content = this.nextElementSibling;
            if (content && content.classList.contains('learn-more-content')) {
                if (content.style.display === 'none') {
                    content.style.display = 'block';
                    content.style.opacity = '0';
                    setTimeout(() => {
                        content.style.opacity = '1';
                    }, 10);
                } else {
                    content.style.opacity = '0';
                    setTimeout(() => {
                        content.style.display = 'none';
                    }, 300);
                }
            }
        });
    });
}

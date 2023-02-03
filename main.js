const hypnospaceStyle = document.getElementById("hypnospaceStyle");

function toggleHidden(elementIDs) {
    elementIDs.forEach(elementID => {
        document.getElementById(elementID).classList.toggle('hidden');
    });
}

function toggleCollapsed(sourceElement) {
    if(sourceElement.textContent == 'See More') {
        sourceElement.textContent = 'See Less';
    }
    else {
        sourceElement.textContent = 'See More';
    }
    sourceElement.parentElement.classList.toggle('collapsed');
}

function toggleHypnospace() {
    hypnospaceStyle.disabled = !hypnospaceStyle.disabled;
}
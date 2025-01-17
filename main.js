const hypnospaceStyle = document.getElementById("hypnospaceStyle");
const secret = document.getElementById("Secret");
let secretCounter = 1;

function toggleHidden(elementIDs) {
    elementIDs.forEach(elementID => {
        document.getElementById(elementID).classList.toggle('hidden');
    });
}

function toggleCollapsed(sourceElement) {
    if(sourceElement.textContent.trim() == 'See More') {
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
document.querySelector('#hypnospace .textOverlay').addEventListener('click', toggleHypnospace);

function incrementSecret() {
    if(secretCounter >= 4 ) {
        secret.classList.toggle('hidden');
    }
    else {
        secretCounter = secretCounter + 1;
    }
}
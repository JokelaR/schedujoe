const hypnospaceStyle = document.getElementById("hypnospaceStyle");
const umineko = document.getElementById("uminekoSecret");
let umiCounter = 1;

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

function incrementUmineko() {
    if(umiCounter >= 12 ) {
        umineko.classList.toggle('hidden');
    }
    else {
        umiCounter = umiCounter + 1;
    }
}
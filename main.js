function toggleHidden(elementIDs) {
    elementIDs.forEach(elementID => {
        document.getElementById(elementID).classList.toggle('hidden');
    });
    
}
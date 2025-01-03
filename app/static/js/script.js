let selectedCell = null;

document.querySelectorAll('.cell').forEach(cell => {
    cell.addEventListener('click', () => {
        const row = cell.dataset.row;
        const col = cell.dataset.col;

        if (selectedCell) {
            fetch('/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    from: [parseInt(selectedCell.dataset.row), parseInt(selectedCell.dataset.col)],
                    to: [parseInt(row), parseInt(col)]
                })
            })
            .then(response => response.json())
            .then(data => {
                showNotification(data.message);  // Show notification instead of alert
                if (data.success) {
                    location.reload();
                }
            });

            selectedCell = null;
            clearHighlights();
        } else {
            selectedCell = cell;
            fetch('/valid-moves', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pos: [parseInt(row), parseInt(col)] })
            })
            .then(response => response.json())
            .then(data => highlightMoves(data.valid_moves));
        }
    });
});

function highlightMoves(moves) {
    console.log(moves);  // Debugging line to inspect moves
    clearHighlights();
    moves.forEach(move => {
        const cell = document.querySelector(`.cell[data-row="${7 - Math.floor(move / 8)}"][data-col="${move % 8}"]`);
        if (cell) cell.classList.add('highlight');
    });
}

function clearHighlights() {
    document.querySelectorAll('.cell').forEach(cell => cell.classList.remove('highlight'));
}

function showNotification(message) {
    // Create the notification element if it doesn't exist
    let notification = document.getElementById('notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'notification';
        document.body.appendChild(notification);
    }

    // Set the notification message
    notification.textContent = message;

    // Make the notification visible
    notification.style.display = 'block';

    // Hide the notification after 3 seconds
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

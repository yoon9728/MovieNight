document.addEventListener('DOMContentLoaded', function() {
    var showMoreButton = document.getElementById('show-more');
    var currentPage = 1;

    showMoreButton.addEventListener('click', function() {
        currentPage++;  // Increment to get the next page

        var xhr = new XMLHttpRequest();
        xhr.open('GET', '?page=' + currentPage, true);
        xhr.onload = function() {
            if (this.status === 200) {
                var newMovies = JSON.parse(this.responseText).html;
                var moviesContainer = document.getElementById('movies-container');
                if (moviesContainer) {
                    moviesContainer.innerHTML += newMovies;
                }
            }
        };
        xhr.send();
    });
});

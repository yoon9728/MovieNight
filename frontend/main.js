let selectedGenres = [];
let currentPage = 1;
let currentSort = 'Popularity';
let searchQuery = '';

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.genre-button').forEach(button => {
        button.addEventListener('click', function() {
            const genre = button.textContent.trim();
            const index = selectedGenres.indexOf(genre);
            if (index >= 0) {
                selectedGenres.splice(index, 1);
                button.classList.remove('red-background');
            } else {
                selectedGenres.push(genre);
                button.classList.add('red-background');
            }
            currentPage = 1;
            loadMovies();
        });
    });

    document.querySelectorAll('[data-sort]').forEach(element => {
        element.addEventListener('click', function() {
            const sortType = this.getAttribute('data-sort');
            currentPage = 1;
            currentSort = sortType;
            loadMovies();
        });
    });

    function changeSort(sortType) {
        currentSort = sortType;
        loadMovies();
    }

    const loadButton = document.getElementById('Load-button');
    if (loadButton) {
        loadButton.addEventListener('click', function() {
            currentPage = 1;
            loadMovies();
        });
    }


    const showMoreButton = document.getElementById('show-more-button');
    if (showMoreButton) {
        showMoreButton.addEventListener('click', function() {
            currentPage += 1;
            loadMovies();
        });
    }

    const searchForm = document.querySelector('form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault();
            searchQuery = document.querySelector('input[type="search"]').value.trim();
            currentPage = 1;
            loadMovies();
        });
    }

    function loadMovies() {
        let genresQuery = selectedGenres.length ? selectedGenres.map(genre => `genres=${encodeURIComponent(genre)}`).join('&') : '';
        let sortQuery = `sort=${currentSort}`;
        let searchQueryPart = searchQuery ? `&search=${encodeURIComponent(searchQuery)}` : '';
        const pageQuery = `page=${currentPage}`;
        let fullQuery = `${genresQuery}&${pageQuery}&${sortQuery}${searchQueryPart}`;
    
        fetch(`/load-movies?${fullQuery}`)
            .then(response => response.json())
            .then(data => {
                if (currentPage === 1) {
                    document.getElementById('movies-container').innerHTML = '';
                }
                addMoviesToPage(data.movies);
    
                const showMoreButton = document.getElementById('show-more-button');
                if (data.has_next) {
                    showMoreButton.style.display = 'block';
                } else {
                    showMoreButton.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    function addMoviesToPage(movies) {
        const moviesContainer = document.getElementById('movies-container');
        movies.forEach(movie => {
            moviesContainer.appendChild(createMovieCard(movie));
        });
    }

    function formatYear(dateString) {
        const date = new Date(dateString);
        return date.getFullYear();
    }

    function slugify(text) {
        return text.toString().toLowerCase()
            .replace(/\s+/g, '-')
            .replace(/[^\w\-]+/g, '')
            .replace(/\-\-+/g, '-')
            .replace(/^-+/, '')
            .replace(/-+$/, '');
    }

    function createMovieCard(movie) {
        const releaseYear = movie.release_date ? formatYear(movie.release_date) : 'YYYY';
        const movieCard = document.createElement('div');
        const movieDetailUrl = `/${"movieDetail"}/${encodeURIComponent(slugify(movie.title))}/${movie.TMDB_id}`;
        movieCard.className = 'movie-card relative flex flex-col shadow-md rounded-xl overflow-hidden hover:shadow-lg hover:-translate-y-1 transition-all duration-300 max-w-md';

        const imdbIconUrl = '/static/icon/imdb.png';

        movieCard.innerHTML = `
            <a href="${movieDetailUrl}" class="movie-card-link">
            <div style="height: 300px; overflow: hidden;">
                <img src="${movie.poster_url}" alt="${movie.title}" style="width:100%; height:100%; object-fit:fit;" class="movie-poster">
            </div>
            <div class="bg-white py-4 px-3">
                <h3 class="text-2xl mb-2 font-medium">${movie.title}</h3>
                <div class="flex justify-between items-center mb-4">
                    <p class="text-sm text-gray-600">
                        ${movie.genres.join(', ')}
                    </p>
                </div>
                <div class="flex items-center justify-end">
                    <p class="movie-year text-lg">${releaseYear}</p>
                    <img src="${imdbIconUrl}" alt="IMDb Icon" class="w-10 h-5">
                    <span class="ml-1 mr-2 text-lg">${movie.IMDB_rating} / 10</span>
                </div>
            </div>
            </a>
        `;

        return movieCard;
    }
});

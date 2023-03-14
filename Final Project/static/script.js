document.addEventListener('DOMContentLoaded', () => {
    const mediaTypes = document.querySelectorAll('.btn-group button');
    mediaTypes.forEach(mediaType => {
        mediaType.addEventListener('click', () => {
            mediaTypes.forEach(mediaType => {
                mediaType.classList.remove('active');
            })

            mediaType.classList.add('active');
        })
    })

    const moviesButton = document.getElementById('movies-button');
    const moviesRows = document.querySelectorAll('.movies-row');

    const seriesButton = document.getElementById('series-button')
    const seriesRows = document.querySelectorAll('.series-row')

    const seasonsHeader = document.getElementById('seasons-header');

    moviesButton.addEventListener('click', () => {
        seasonsHeader.style.display = 'none';

        moviesRows.forEach(movieRow => {
            movieRow.style = 'table table-hover';
        })

        seriesRows.forEach(serieRow => {
            serieRow.style.display = 'none';
        })
    })

    seriesButton.addEventListener('click', () => {
        seasonsHeader.style.display = 'table-cell';

        moviesRows.forEach(movieRow => {
            movieRow.style.display = 'none';
        })

        seriesRows.forEach(serieRow => {
            serieRow.style = 'table table-hover';
        })
    })

    const removeSelectedMediaButton = document.querySelector('#remove-selected-media-button')
    const resetSelectedMediaButton = document.querySelector('#reset-selected-media-button')

    removeSelectedMediaButton.addEventListener('click', () => {
        const checkedInputs = document.querySelectorAll('input[name="select-media"]:checked');

        const selectedMedias = []
        checkedInputs.forEach(input => {
            const media = (input.value).replaceAll("\'", "\"")
            selectedMedias.push(media)

            var imdbID = JSON.parse(media.replace(/'/g, '"'))["imdbID"];
            var removeMedia = document.getElementById(imdbID);
            removeMedia.style.display = 'none';
            input.checked = false;
        })

        var request = new XMLHttpRequest();
        request.open("POST", "/remove_media");
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.send(JSON.stringify(selectedMedias));
    })


    resetSelectedMediaButton.addEventListener('click', () => {
        const checkedInputs = document.querySelectorAll('input[name="select-media"]:checked');

        const selectedMedias = []
        checkedInputs.forEach(input => {
            const media = (input.value).replaceAll("\'", "\"")
            selectedMedias.push(media)

            var imdbID = JSON.parse(media.replace(/'/g, '"'))["imdbID"];
            var type = JSON.parse(media.replace(/'/g, '"'))["media_type"];
            if (type === "Series") {
                var resetMedia = document.getElementById(imdbID);
                resetMedia.getElementsByClassName('user-season')[0].textContent = 1;
            }

        })

        var request = new XMLHttpRequest();
        request.open("POST", "/reset_media");
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.send(JSON.stringify(selectedMedias));
    })

    const incrementSeasonButtons = document.querySelectorAll('#increment-season');
    incrementSeasonButtons.forEach(incrementSeasonButton => {
        var currentSeason = parseInt(incrementSeasonButton.nextElementSibling.textContent);
        var totalSeasons = parseInt(incrementSeasonButton.parentElement.nextElementSibling.textContent.split("/")[1]);
        if (currentSeason === totalSeasons) {
            incrementSeasonButton.style.display = "none";
        }

        incrementSeasonButton.addEventListener("click", () => {
            var serieId = incrementSeasonButton.dataset.id;
            var currentSeason = parseInt(incrementSeasonButton.nextElementSibling.textContent);
            var totalSeasons = parseInt(incrementSeasonButton.parentElement.nextElementSibling.textContent.split("/")[1]);
            var a = parseInt(incrementSeasonButton.nextElementSibling.textContent)

            if (currentSeason < totalSeasons) {
                var request = new XMLHttpRequest();
                request.open("POST", "/increment_season");
                request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                request.send(JSON.stringify({"id": serieId, "season": currentSeason + 1}));
                incrementSeasonButton.nextElementSibling.textContent = currentSeason + 1;

                if (currentSeason + 1 === totalSeasons) {
                    incrementSeasonButton.style.display = "none";
                }
            }

        })
    })

    const statusSelects = document.querySelectorAll('.status-select');
    statusSelects.forEach(select => {
        select.addEventListener('change', () => {
            const imdbID = select.getAttribute('data-id');
            const status = select.value;

            var request = new XMLHttpRequest();
            request.open("POST", "/update_status");
            request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            request.send(JSON.stringify({"id": imdbID, "status": status}));

        })
    })

})
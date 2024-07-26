document.addEventListener('DOMContentLoaded', function () {
    const audio = document.getElementById('audio1');
    const playButton = document.querySelector('.play1');
    const pauseButton = document.querySelector('.pause1');
    const progressBar = document.querySelector('.progress-bar1');
    const progressContainer = document.querySelector('.progress-container1');

    // Load saved player state from sessionStorage
    const savedAudioTime = sessionStorage.getItem('audioTime');
    const isPlaying = sessionStorage.getItem('isPlaying') === 'true';

    if (savedAudioTime) {
        audio.currentTime = parseFloat(savedAudioTime);
    }

    if (isPlaying) {
        audio.play();
        playButton.style.display = 'none';
        pauseButton.style.display = 'inline-block';
    }

    playButton.addEventListener('click', () => {
        audio.play();
        playButton.style.display = 'none';
        pauseButton.style.display = 'inline-block';
        sessionStorage.setItem('isPlaying', 'true');
    });

    pauseButton.addEventListener('click', () => {
        audio.pause();
        pauseButton.style.display = 'none';
        playButton.style.display = 'inline-block';
        sessionStorage.setItem('isPlaying', 'false');
    });

    audio.addEventListener('timeupdate', () => {
        const progressPercent = (audio.currentTime / audio.duration) * 100;
        progressBar.style.width = `${progressPercent}%`;
        sessionStorage.setItem('audioTime', audio.currentTime);
    });

    progressContainer.addEventListener('click', (e) => {
        const width = progressContainer.clientWidth;
        const clickX = e.offsetX;
        const duration = audio.duration;

        audio.currentTime = (clickX / width) * duration;
        sessionStorage.setItem('audioTime', audio.currentTime);
    });

    // Function to load audio source via AJAX
    function loadAudio(url) {
        fetch(url)
            .then(response => response.blob())
            .then(blob => {
                const newAudioUrl = URL.createObjectURL(blob);
                audio.src = newAudioUrl;
                audio.load();
            })
            .catch(error => console.error('Error loading audio:', error));
    }

    // Example function to fetch new audio file
    function fetchNewAudio() {
        $.ajax({
            url: '/path/to/your/api', // Replace with your API endpoint
            method: 'GET',
            success: function(data) {
                loadAudio(data.audioUrl); // Assume your API returns an object with an audioUrl property
            },
            error: function(xhr, status, error) {
                console.error('Error fetching audio:', error);
            }
        });
    }

    // Call this function when you need to load new audio
    fetchNewAudio();

    // Additional functionalities for file upload and button states
    function showFileName(event) {
        const input = event.target;
        const fileName = input.files[0].name;
        document.getElementById('file-label').textContent = `Selected file: ${fileName}`;
        document.getElementById('upload-btn').disabled = false;
    }

    function showDownloadButton(url) {
        const downloadButton = document.getElementById('download-btn');
        const audioButton = document.getElementById('audio');
        audioButton.src = url;
        downloadButton.href = url;
        downloadButton.style.display = 'inline-block';
    }

    document.getElementById('maleBtn').addEventListener('click', function () {
        document.getElementById('maleOptions').style.display = 'block';
        document.getElementById('femaleOptions').style.display = 'none';
    });

    document.getElementById('femaleBtn').addEventListener('click', function () {
        document.getElementById('femaleOptions').style.display = 'block';
        document.getElementById('maleOptions').style.display = 'none';
    });

    document.getElementById('all_done').addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(event.target);

        try {
            const response = await fetch(event.target.action, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const jsonResponse = await response.json();
            showPopup(jsonResponse.message);

            // Show the download button
            const downloadUrl = jsonResponse.download_url;
            showDownloadButton(downloadUrl);

            event.target.reset();
        } catch (error) {
            console.error('Error:', error);
            showPopup('File upload failed. Please try again.');
        }
    });

    function showPopup(message) {
        const popup = document.getElementById('popupModal');
        document.getElementById('popupMessage').textContent = message;
        popup.style.display = 'block';
    }

    function closePopup() {
        const popup = document.getElementById('popupModal');
        popup.style.display = 'none';
    }

    const conversion_type = document.getElementById('conversion-type');
    const male_to_female_button = document.getElementById('male_to_female');
    const male_to_child_button = document.getElementById('male_to_child');
    const female_to_male_button = document.getElementById('female_to_male');
    const female_to_child_button = document.getElementById('female_to_child');

    male_to_female_button.addEventListener('click', function(){
        conversion_type.value = 'male_to_female';
        male_to_female_button.style.backgroundColor = 'blue';
        male_to_child_button.style.backgroundColor = '';
    });

    male_to_child_button.addEventListener('click', function(){
        conversion_type.value = 'male_to_child';
        male_to_child_button.style.backgroundColor = 'blue';
        male_to_female_button.style.backgroundColor = '';
    });

    female_to_male_button.addEventListener('click', function(){
        conversion_type.value = 'female_to_male';
        female_to_male_button.style.backgroundColor = 'blue';
        female_to_child_button.style.backgroundColor = '';
    });

    female_to_child_button.addEventListener('click', function(){
        conversion_type.value = 'female_to_child';
        female_to_child_button.style.backgroundColor = 'blue';
        female_to_male_button.style.backgroundColor = '';
    });

    function loadHtmlContent(url, containerId) {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                document.getElementById(containerId).innerHTML = html;
                initializeAudioPlayer(); // Initialize the audio player if needed
            })
            .catch(error => console.error('Error loading HTML content:', error));
    }

    // Initialize audio player if required
    function initializeAudioPlayer() {
        // Your audio player initialization code here
    }

    // Load the content from audio-player.html
    loadHtmlContent("{% static 'audio-player.html' %}", "audio-player-container");
});

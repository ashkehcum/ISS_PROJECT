// // ************************ Drag and drop ***************** //
// let dropArea = document.getElementById("drop-area")

//     // Prevent default drag behaviors
//     ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
//         dropArea.addEventListener(eventName, preventDefaults, false)
//         document.body.addEventListener(eventName, preventDefaults, false)
//     })

//     // Highlight drop area when item is dragged over it
//     ;['dragenter', 'dragover'].forEach(eventName => {
//         dropArea.addEventListener(eventName, highlight, false)
//     })

//     ;['dragleave', 'drop'].forEach(eventName => {
//         dropArea.addEventListener(eventName, unhighlight, false)
//     })

// // Handle dropped files
// dropArea.addEventListener('drop', handleDrop, false)

// function preventDefaults(e) {
//     e.preventDefault()
//     e.stopPropagation()
// }

// function highlight(e) {
//     dropArea.classList.add('highlight')
// }

// function unhighlight(e) {
//     dropArea.classList.remove('active')
// }

// function handleDrop(e) {
//     var dt = e.dataTransfer
//     var files = dt.files

//     handleFiles(files)
// }

// let uploadProgress = []
// let progressBar = document.getElementById('progress-bar')

// function initializeProgress(numFiles) {
//     progressBar.value = 0
//     uploadProgress = []

//     for (let i = numFiles; i > 0; i--) {
//         uploadProgress.push(0)
//     }
// }

// function updateProgress(fileNumber, percent) {
//     uploadProgress[fileNumber] = percent
//     let total = uploadProgress.reduce((tot, curr) => tot + curr, 0) / uploadProgress.length
//     progressBar.value = total
// }

// function handleFiles(files) {
//     files = [...files]
//     initializeProgress(files.length)
//     files.forEach(uploadFile)
//     files.forEach(previewFile)
// }

// // function previewFile(file) {
// //     let reader = new FileReader()
// //     reader.readAsDataURL(file)
// //     reader.onloadend = function () {
// //         let img = document.createElement('img')
// //         img.src = reader.result
// //         document.getElementById('gallery').appendChild(img)
// //     }
// // }

// function previewFile(file) {
//     let reader = new FileReader();
//     reader.readAsDataURL(file);
//     reader.onloadend = function () {
//         let container = document.createElement('div'); // Create a container for the image
//         container.classList.add('image-container');
        
//         let img = document.createElement('img');
//         img.src = reader.result;
//         container.appendChild(img); // Append the image to the container
        
//         let deleteBtn = document.createElement('button'); // Create a delete button
//         deleteBtn.textContent = '×'; // Add a cross symbol
//         // deleteBtn.textContent = '*';
//         deleteBtn.classList.add('delete-btn');
//         deleteBtn.addEventListener('click', function () {
//             container.remove(); // Remove the container when the delete button is clicked
//         });
//         container.appendChild(deleteBtn); // Append the delete button to the container
        
//         document.getElementById('gallery').appendChild(container); // Append the container to the gallery
//     };
// }



// function uploadFile(file, i) {
//     var url = 'https://api.cloudinary.com/v1_1/joezimim007/image/upload'
//     var xhr = new XMLHttpRequest()
//     var formData = new FormData()
//     xhr.open('POST', url, true)
//     xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest')

//     // Update progress (can be used to show progress indicator)
//     xhr.upload.addEventListener("progress", function (e) {
//         updateProgress(i, (e.loaded * 100.0 / e.total) || 100)
//     })

//     xhr.addEventListener('readystatechange', function (e) {
//         if (xhr.readyState == 4 && xhr.status == 200) {
//             updateProgress(i, 100) // <- Add this
//         }
//         else if (xhr.readyState == 4 && xhr.status != 200) {
//             // Error. Inform the user
//         }
//     })

//     formData.append('upload_preset', 'ujpu6gyk')
//     formData.append('file', file)
//     xhr.send(formData)
// }


let dropArea = document.getElementById("drop-area");
let photoCounter = 0; // Initialize photo counter

// Prevent default drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

// Highlight drop area when item is dragged over it
['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
});

// Handle dropped files
dropArea.addEventListener('drop', handleDrop, false);

let uploadProgress = [];
let progressBar = document.getElementById('progress-bar');

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    dropArea.classList.add('highlight');
}

function unhighlight(e) {
    dropArea.classList.remove('active');
}

function initializeProgress() {
    progressBar.value = 0; // Reset the progress bar value to 0
    uploadProgress = [];
}

function updateProgress(fileNumber, percent) {
    uploadProgress[fileNumber] = percent;
    let total = uploadProgress.reduce((tot, curr) => tot + curr, 0) / uploadProgress.length;
    progressBar.value = total;
}

function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files;
    initializeProgress(); // Reset progress bar before handling new files
    files = [...files];
    files.forEach(uploadFile);
    files.forEach(previewFile);
    photoCounter += files.length; // Increment photo counter by the number of files dropped
    updatePhotoCounter(); // Update the displayed photo counter
}

// function previewFile(file) {
//     let reader = new FileReader();
//     reader.readAsDataURL(file);
//     reader.onloadend = function () {
//         let container = document.createElement('div'); // Create a container for the image
//         container.classList.add('image-container');

//         let img = document.createElement('img');
//         img.src = reader.result;
//         container.appendChild(img); // Append the image to the container

//         let deleteBtn = document.createElement('button'); // Create a delete button
//         deleteBtn.textContent = '×'; // Add a cross symbol
//         // deleteBtn.innerHTML = '<i class="fas fa-times"></i>'; // Use Font Awesome times icon

//         deleteBtn.classList.add('delete-btn');
//         deleteBtn.addEventListener('click', function () {
//             container.remove(); // Remove the container when the delete button is clicked
//             photoCounter--; // Decrease photo counter when a photo is deleted
//             updatePhotoCounter(); // Update the displayed photo counter
//         });
//         container.appendChild(deleteBtn); // Append the delete button to the container

//         document.getElementById('gallery').appendChild(container); // Append the container to the gallery
//     };
// }
function previewFile(file) {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function () {
        let container = document.createElement('div'); // Create a container for the image
        container.classList.add('image-container');

        let img = document.createElement('img');
        img.src = reader.result;
        container.appendChild(img); // Append the image to the container

        let deleteBtn = document.createElement('button'); // Create a delete button
        deleteBtn.classList.add('delete-btn');
        deleteBtn.innerHTML = '<i class="fas fa-times"></i>'; // Use Font Awesome times icon
        deleteBtn.addEventListener('click', function () {
            container.remove(); // Remove the container when the delete button is clicked
            photoCounter--; // Decrease photo counter when a photo is deleted
            updatePhotoCounter(); // Update the displayed photo counter
        });
        container.appendChild(deleteBtn); // Append the delete button to the container

        document.getElementById('gallery').appendChild(container); // Append the container to the gallery
    };
}




function uploadFile(file, i) {
    let url = 'https://api.cloudinary.com/v1_1/joezimim007/image/upload';
    let xhr = new XMLHttpRequest();
    let formData = new FormData();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    // Update progress (can be used to show progress indicator)
    xhr.upload.addEventListener("progress", function (e) {
        updateProgress(i, (e.loaded * 100.0 / e.total) || 100);
    });

    xhr.addEventListener('readystatechange', function (e) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            updateProgress(i, 100); // <- Add this
        } else if (xhr.readyState == 4 && xhr.status != 200) {
            // Error. Inform the user
        }
    });

    formData.append('upload_preset', 'ujpu6gyk');
    formData.append('file', file);
    xhr.send(formData);
}

function updatePhotoCounter() {
    document.getElementById('photo-counter').textContent = `Number of Photos Uploaded: ${photoCounter}`;
}

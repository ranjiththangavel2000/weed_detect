import React, { useState } from 'react';
import './App.css';

function App() {
  const [imageUrl, setImageUrl] = useState('');
  const [resultMessage, setResultMessage] = useState('');
  const [isResultVisible, setIsResultVisible] = useState(false);
  const [isLoading, setIsLoading] = useState(false); // New state for loading

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = function () {
        setImageUrl(reader.result);
        setIsResultVisible(false);
      };
    }
  };

  const handleAnalyzeClick = () => {
    // Set loading state to true to display the loading spinner
    setIsLoading(true);
  
    // Simulate a delay of 5 seconds before making the API call
    setTimeout(() => {
      // Perform the API call here
      const file = document.getElementById('imageUpload').files[0];
      const formData = new FormData();
      formData.append('file', file);
  
      fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          // Update state or perform actions based on API response
          console.log(data);
          setResultMessage(`Analysis Result: ${data.result}`);
          setIsResultVisible(true);
  
          // Set loading state back to false
          setIsLoading(false);
        })
        .catch((error) => {
          console.error('Error analyzing image:', error);
          setResultMessage('Error analyzing image.');
          setIsResultVisible(true);
  
          // Set loading state back to false
          setIsLoading(false);
        });
    }, 5000); // Simulated delay of 5 seconds
  };
  

  return (
    <>
      <center>
      <div className="content">
        <h1>🌿WEEDS DETECTION🌿</h1>
        <div id="uploadContainer">
          <input type="file" id="imageUpload" accept="image/*" onChange={handleImageUpload} />
          <label htmlFor="imageUpload"></label>
          <button id='btn' onClick={handleAnalyzeClick}>Analyze Image</button>
        </div>
        {imageUrl && (
          <div id="imagePreviewContainer">
            <h2 id='ipc'>UPLOAD IMAGE:</h2>
            <img id="imagePreview" src={imageUrl} alt="Uploaded" />
          </div>
        )}
        {isLoading && ( // Display loading animation if isLoading is true
            <div className="loading-container">
              <div className="loading-spinner"></div>
            </div>
          )}
        {isResultVisible && (
          <div id="resultContainer">
            <h2>ANALYSIS RESULT:</h2>
            <div id="resultText">{resultMessage}</div>
          </div>
        )}
      </div>
      </center> 
    </>
  );
}

export default App;

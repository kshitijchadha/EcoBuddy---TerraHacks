<script>
  import { onMount } from "svelte";

  let video;
  let canvas;
  let context;
  let photo;
  let hasCamera = false;

  let output_message = "";
  let loading = false; 
  let text_color = "white"

  $: {
    if (output_message.endsWith("TRASH")) {
      text_color = "stone-400";
    } else if (output_message.endsWith("RECYCLE")) {
      text_color = "cyan-400";
    } else if (output_message.endsWith("COMPOST")) {
      text_color = "lime-400"
    } else {
      text_color = "white"
    }
  }
  
  // Initialize the camera and video stream
  async function startCamera() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      video.srcObject = stream;
      video.play();
      hasCamera = true;
    } catch (err) {
      console.error('Error accessing the camera', err);
    }
  }
  onMount(async () => {
    await startCamera();
  });
  
  // Capture a photo from the video stream
  function capturePhoto() {
    if (!video || !canvas) return;
  
    // Initialize the canvas context
    context = canvas.getContext('2d');
    
    // Check if context is initialized properly
    if (context) {
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      photo = canvas.toDataURL('image/png');
      
      // Convert and send the photo
      convertAndSendPhoto(photo);
    } else {
      console.error('Failed to get canvas context');
    }
  }
  
  // Convert data URL to Blob and send it as a file with key 'image'
  async function convertAndSendPhoto(dataUrl) {
    // Convert data URL to Blob
    loading = true; 
    const response = await fetch(dataUrl);
    const blob = await response.blob();
    
    // Create a FormData object
    const formData = new FormData();
    formData.append('image', blob, 'photo.png'); // Use 'image' as the key
    
    try {
      // Send the photo to the API
      const apiResponse = await fetch('http://127.0.0.1:5000/api/classify_image', {
        method: 'POST',
        body: formData
      });
      
      if (apiResponse.ok) {
        const result = await apiResponse.json();
        loading = false;
        console.log('Upload successful:', result, result.message);
        output_message = result.message;
      } else {
        console.error('Upload failed:', apiResponse.statusText);
      }
    } catch (err) {
      console.error('Error uploading photo:', err);
    }
  }
</script>

<div class="w-1/2 mx-auto">
  <div>
    <h1 class='text-3xl font-bold text-{text_color} text-center my-4'>{output_message}</h1>
  </div>

  <video style="width: 100%; display: block;" bind:this={video}>
    <track kind="captions" srclang="en" label="English" default>
    Your browser does not support the video tag.
  </video>
  <canvas class="hidden" bind:this={canvas} width="640" height="480"></canvas>   
  
  <div class="flex my-4">
    {#if hasCamera}
      <button class="btn btn-primary" on:click={capturePhoto}>Capture Photo</button>
    {/if}

    {#if loading}
      <div class="spinner-border ml-10" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    {/if}
  </div>
</div>
  
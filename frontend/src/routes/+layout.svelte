<script>
  import Navbar from "../lib/Navbar.svelte";
</script>

<body class="bg-emerald-800 h-[100%]">
  <Navbar />
  <main>
    <slot></slot>
  </main>   
</body>

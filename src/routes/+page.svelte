<script>
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
  
    onMount(() => {
      if (browser) {
        const user = $page.data.session?.user;
        
        if (user) {
          // User is authenticated, redirect to private path
          goto('/private');
        } else {
          // User is not authenticated, redirect to auth path
          goto('/auth');
        }
      }
    });
  </script>
  
  <div>
    Redirecting...
  </div>
  
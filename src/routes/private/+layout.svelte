<script>
    import { goto } from '$app/navigation';
    export let data;
    $: ({ supabase } = data);

    $: logout = async () => {
        const { error } = await supabase.auth.signOut();
        if (error) {
            console.error(error);
        } else {
            // Redirect to the auth page after successful logout
            goto('/auth');
        }
    };
</script>

<header>
    <nav>
        <a href="/">Home</a>
    </nav>
    <button on:click={logout}>Logout</button>
</header>
<main>
    <slot />
</main>

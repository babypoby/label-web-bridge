<script>
    export let value = null;
    export let options = ["Yes", "No", "Not Applicable"];

    function handleClick(option) {
        return () => {
            value = value === option ? null : option;
        }
    }
</script>

<div class="button-container">
    {#each options as option}
        <button 
            class:selected={value === option}
            on:click={handleClick(option)}
        >
            {option}
        </button>
    {/each}
</div>

<style>
    .button-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
    }

    button {
        padding: 0.5rem 1rem;
        font-size: 1rem;
        cursor: pointer;
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        border-radius: 4px;
        transition: background-color 0.3s, opacity 0.01s;
    }

    button.selected {
        background-color: #4CAF50;
        color: white;
    }

    button.selected:nth-child(2) {
        background-color: rgb(227, 78, 78);
    }

    button.selected:nth-child(3) {
        background-color: #FFA500;
    }
</style>

<script>
    export let value = null;
  
    function handleClick(option) {
        return () => (value = value === option ? null : option)
        // value = value === option ? null : option;
        value = true
    }
</script>
  
<div class="button-container">
    <button 
        class:selectedtrue={value === true}
        on:click={handleClick(true)}
    >
        Yes
    </button>
    <button 
        class:selectedfalse={value === false}
        on:click={handleClick(false)}
    >
        No
    </button>
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
  
    button.selectedtrue {
        background-color: #4CAF50;
        color: white;
    }

    button.selectedfalse {
        background-color: rgb(227, 78, 78);
        color: white;
    }
</style>

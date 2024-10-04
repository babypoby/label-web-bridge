<!-- ProgressBar.svelte -->
<script lang="ts">
    export let current: number;
    export let total: number = 300;

    $: percentage = Math.min((current / total) * 100, 100);
</script>

<div class="progress-container">
    <div class="progress-bar" style="width: {percentage}%"></div>
    <div class="progress-text">{current} / {total} conversations rated</div>
</div>

<style>
    .progress-container {
        width: 100%;
        background-color: #f9f9f9;
        border-radius: 5px;
        margin-bottom: 20px;
        position: relative;
        height: 30px;
        border: 1px solid #ddd;
        border-radius: 5px;
    }

    .progress-bar {
        height: 100%;
        background-color: #427afd;
        border-radius: 5px;
        transition: width 0.5s ease-in-out;
    }

    .progress-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #333;
    }
</style>

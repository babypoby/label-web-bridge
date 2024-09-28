<script lang="ts">
    import { createClient } from "@supabase/supabase-js";
    import SelectButton from "./SelectButton.svelte";
    import { onMount, afterUpdate } from "svelte";
    import { page } from '$app/stores';
    import type { Database } from "./supabase-types";


    export let conversation;
    

    const supabase = createClient<Database>(
        "https://jryeokpjkidbgzscmrcj.supabase.co",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpyeWVva3Bqa2lkYmd6c2NtcmNqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU5ODQ3NjIsImV4cCI6MjA0MTU2MDc2Mn0.nLeYIrrnbkSVqKeY7XOZkgHxDYwDcQOSVwmzrZgQrMo",
    );

    let rubric_1, rubric_2, rubric_3, rubric_4 = null;

    function resetRatings() {
        rubric_1 = null;
        rubric_2 = null;
        rubric_3 = null;
        rubric_4 = null;
    }

    $: {
        if (conversation) {
            resetRatings();
        }
    }

    $: isFormComplete =
    rubric_1 !== null &&
    rubric_2 !== null &&
    rubric_3 !== null &&
    rubric_4 !== null;

   

    let user;

    $: user = $page.data.session?.user;

    async function submitRating() {
    if (!user) {
        alert("You must be logged in to submit a rating.");
        return;
    }

    if (!isFormComplete) {
        alert("Please complete all ratings before submitting.");
        return;
    }

    try {
        const { data, error } = await supabase
            .from("rating")
            .upsert({
                conversation_id: conversation.conversation_id,
                user_id: user.id,
                rubric_1,
                rubric_2,
                rubric_3,
                rubric_4,
            })
            .select();

        if (error) throw error;

        if (data && data.length > 0) {
            alert("Rating submitted successfully!");
        } else {
            throw new Error("No data returned after upsert");
        }
    } catch (error) {
        console.error("Error submitting rating:", error);
        alert("Error submitting rating. Please try again.");
    }
}

     

    onMount(() => {
        resetRatings();
    });
</script>

<div class="container">
    <div class="conversation-box">
        <h3>Conversation</h3>
        {#each conversation.convos as convo}
            <p><strong>{convo.user.toUpperCase()}:</strong> {convo.text}</p>
        {/each}
    </div>
    <div class="response-box">
        <h3>Tutor Response:</h3>
        {#each conversation.responses as response}
            <p>{response.text}</p>
        {/each}
    </div>
    <div class="rating-box">
        <h3>Rate this conversation</h3>
        <p class="instruction">
            For the following attributes, please annotate if the tutor should
            demonstrate the attribute at their specific point of progress in the
            conversation, and then whether the tutor actually demonstrates that
            attribute.
        </p>

        <!--<div class="attribute">
            <p>
                Explains the underlying concepts or skills in a clear way that
                is easy for the student to understand
            </p>
            <div class="rating-row">
                <span>Should demonstrate:</span>
                <SelectButton bind:value={explains_concepts_0} />
            </div>
            <div class="rating-row">
                <span>Actually demonstrates:</span>
                <SelectButton bind:value={explains_concepts_1} />
            </div>
        </div>-->

        <div class="attribute">
            <p>
                Inspires and stimulates the interest or curiosity of the student
            </p>
            <div class="rating-row">
                <span>Should demonstrate:</span>
                <SelectButton bind:value={rubric_1} />
            </div>
            <div class="rating-row">
                <span>Actually demonstrates:</span>
                <SelectButton bind:value={rubric_2} />
            </div>
        </div>

        <div class="attribute">
            <p>
                Monitors the student's motivational state and adjusts responses
                accordingly
            </p>
            <div class="rating-row">
                <span>Should demonstrate:</span>
                <SelectButton bind:value={rubric_3} />
            </div>
            <div class="rating-row">
                <span>Actually demonstrates:</span>
                <SelectButton bind:value={rubric_4} />
            </div>
        </div>

        <!--<div class="attribute">
            <p>
                Delivers feedback (whether positive or negative) in an
                encouraging way
            </p>
            <div class="rating-row">
                <span>Should demonstrate:</span>
                <SelectButton bind:value={speaks_encouragingly_0} />
            </div>
            <div class="rating-row">
                <span>Actually demonstrates:</span>
                <SelectButton bind:value={speaks_encouragingly_1} />
            </div>
        </div>

        <div class="attribute">
            <p>Identifies the student's goal or prior knowledge</p>
            <div class="rating-row">
                <span>Should demonstrate:</span>
                <SelectButton bind:value={identifies_goal_0} />
            </div>
            <div class="rating-row">
                <span>Actually demonstrates:</span>
                <SelectButton bind:value={identifies_goal_1} />
            </div>
        </div>-->
    </div>
    <div class="button-container">
        <button on:click={submitRating} disabled={!isFormComplete}
            >Submit</button
        >
    </div>
</div>

<style>
    .container {
        max-width: 800px;
        margin: 0 auto;
        font-family: Arial, sans-serif;
    }
    .conversation-box,
    .response-box,
    .rating-box {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 5px;
        margin: 20px 0;
        padding: 20px;
    }
    h3 {
        margin-top: 0;
        color: #333;
    }
    .instruction {
        font-style: italic;
        color: #666;
    }
    .attribute {
        margin-bottom: 20px;
    }
    .rating-row {
        display: flex;
        align-items: center;
        margin: 10px 0;
    }
    .rating-row span {
        width: 200px;
    }
    button {
        background-color: #427afd;
        border: none;
        color: white;
        padding: 15px 25px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 18px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 10px;
        transition: background-color 0.3s;
    }
    button:hover {
        background-color: #3062d7;
    }
    button:disabled {
        background-color: #cccccc;
        cursor: not-allowergb(155, 155, 155);
        color: white;
    }

    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
</style>

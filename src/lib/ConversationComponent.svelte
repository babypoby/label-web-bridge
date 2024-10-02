<script lang="ts">
    import SelectButton from "./SelectButton.svelte";
    import { onMount } from "svelte";
    import type { Database } from "./supabase-types";
    import { page } from "$app/stores";

    export let conversation;
    
    const supabase = $page.data.supabase
/* 
    const supabase = createClient<Database>(
        "https://jryeokpjkidbgzscmrcj.supabase.co",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpyeWVva3Bqa2lkYmd6c2NtcmNqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU5ODQ3NjIsImV4cCI6MjA0MTU2MDc2Mn0.nLeYIrrnbkSVqKeY7XOZkgHxDYwDcQOSVwmzrZgQrMo",
    ); */

    let rubrics = [null, null, null, null, null];

    function resetRatings() {
        rubrics = rubrics.map(() => null);
    }

    $: {
        if (conversation) {
            resetRatings();
        }
    }

    $: isFormComplete = rubrics.every(rubric => rubric !== null);

    let user;

    onMount(async () => {
        const { data: { user: authUser }, error } = await supabase.auth.getUser();
        if (error) {
            console.error('Error fetching user:', error);
        } else {
            user = authUser;
        }
        resetRatings();
    });

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
                    rubric_1: rubrics[0],
                    rubric_2: rubrics[1],
                    rubric_3: rubrics[2],
                    rubric_4: rubrics[3],
                    rubric_5: rubrics[4]
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

    let showInfo = {
        1: false,
        2: false,
        3: false,
        4: false,
        5: false
    };

    let showExamples = {
        1: false,
        2: false,
        3: false,
        4: false,
        5: false
    };

    function toggleInfo(index) {
        showInfo[index] = !showInfo[index];
        if (showInfo[index]) showExamples[index] = false;
    }

    function toggleExamples(index) {
        showExamples[index] = !showExamples[index];
        if (showExamples[index]) showInfo[index] = false;
    }

    function getQuestionText(index) {
        const questions = [
            "Does the Tutor give away the answer?",
            "Does the Tutor promote active engagement?",
            "Is the Tutor considerate of the Student's expressed feelings?",
            "Does the Tutor have a positive tone?",
            "Does the Tutor point out the Student's mistake?"
        ];
        return questions[index - 1];
    }

    function getInfoText(index) {
    const infoTexts = [
        `
        The Tutor must never give away the answer in full. Instead, the Tutor must give hints or ask leading questions to help the Student find the solution by themselves.

        • Answer "Yes" if:
          - The Tutor gives away the answer, even if they ask a question afterward.
          - The Student's statement is partially true, and the Tutor explains why it's only partially correct or what the exceptions are.

        • Answer "Not Applicable" when:
          - The Student did not attempt to give an answer to a question in the previous utterance.
          - The Teacher confirms that the Student is correct.
        `,
        `
        The Tutor must promote active engagement from the Student. This can be done by:

        • Asking follow-up questions to dig deeper
        • Asking whether the Student would like to learn more
        • Asking the Student to try something for themselves
        • Providing practice problems
        `,
        `
        The Tutor must be considerate of the Student's expressed feelings, respond appropriately, and adapt the flow of the lesson accordingly.

        Important: Only take into account explicitly expressed feelings. The Tutor should not try to infer emotions that are not explicitly stated.

        • Examples of words describing emotions: tired, proud, happy, confused, etc.

        • Answer "Not Applicable" if:
          - The Student did not explicitly state an emotion
          - It is hard to determine whether the emotion was explicitly expressed
        `,
        `
        The Tutor must be highly positive, enthusiastic and encouraging.

        • Answer "Yes" if: The Tutor is highly positive, enthusiastic and encouraging.
        • Answer "No" if: The Tutor is neutral or somewhat positive.
        `,
        `
        The Tutor must point out the Student's mistake when the Student's statement contains a mistake.

        • Answer "Yes" if: The Tutor points out the mistake.

        • Answer "No" if:
          - The Tutor states that the Student's statement is right even though it is not
          - The Tutor does not point out the mistake directly or not at all.
          - The Tutor gives the right answer without pointing out what was wrong

        • Answer "Not Applicable" if:
          - It is not clear whether the Student made a mistake
          - The Student's statement does not contain an answer to a question
        `
    ].map(e => e.split('\n').map(x => x.trim()).join('\n')
    )
    return infoTexts[index - 1];
}


    function getOptions(index) {
        const allOptions = ["Yes", "No", "Not Applicable"];
        return index === 2 || index === 4 ? allOptions.slice(0, 2) : allOptions;
    }

    const examples = {
        1: [
            { Student: "What is the correct syntax for comparing strings in Python?", Tutor: "Have you compared other things before in Python?", critic: "No" },
            { Student: "Will a glass with ice cubes overflow when the cubes melt?", Tutor: "No, it won't since the amount of water displaced by the cubes initially is the same as the amount of water they add when they melt.", critic: "Yes" }
        ],
        2: [
            { Student: "How can I remove the last element from a list in Python?", Tutor: "Let's look at the documentation of a list! What methods might be useful?", critic: "Yes" },
            { Student: "Will a glass with ice cubes overflow when the cubes melt?", Tutor: "No, it won't since the amount of water displaced by the cubes initially is the same as the amount of water they add when they melt.", critic: "No" }
        ],
        3: [
            { Student: "I'm starting to get pretty tired.", Tutor: "Great, let's keep going! Would you like another quiz question?", critic: "No" },
            { Student: "I got that one right too! I feel like I'm on a roll!", Tutor: "Well done! Would you like another question, perhaps an even harder one?", critic: "Yes" }
        ],
        4: [
            { Student: "Can you quiz me?", Tutor: "Ok. What is 1 + 1?", critic: "No" },
            { Student: "Can you quiz me?", Tutor: "Sure I would be happy to! What is 1 + 1?", critic: "Yes" }
        ],
        5: [
            { Student: "Okay I think thylakoid are the cells that contain the chlorophyll in the chloroplast. The stacks of thylakoid are called grana.", Tutor: "Almost there! Thylakoids aren't cells, they are organelles within cell, but everything else is correct. Nicely done!", critic: "Yes" },
            { Student: "I need to multiply everything out so I get (x+3)∗ (x−1) = x^2− 3.", Tutor: "That's great! You need to multiply everything out! Would you like another question?", critic: "No" },
            { Student: "If I push a 2kg object with a force of 10N it will accelerate with 10/2=5m/s!", Tutor: "Nicely done, you applied Newton's law F=m∗a correctly! The answer 5 is correct too, but take another look at the units m/s. Are those the correct units for acceleration?", critic: "Yes" }
        ]
    };
</script>

<div class="container">
    <div class="conversation-box">
        <h3>Conversation</h3>
        {#each conversation.convos as convo}
            <p><strong>{convo.user.toUpperCase()}:</strong> {convo.text}</p>
        {/each}
    </div>
    <!-- Add this block after the conversation-box -->
    {#if conversation.conversation_id.split('_').length === 2}
        <div class="student-status">
            <p><strong>Note:</strong> The student is currently incorrect.</p>
        </div>
    {/if}
    <div class="response-box">
        <h3>Tutor Response:</h3>
        {#each conversation.responses as response}
            <p>{response.text}</p>
        {/each}
    </div>
    <div class="rating-box">
        <h3>Rate this conversation</h3>
        <p class="instruction">
            You are a Critic giving feedback on the Tutor's Tutoring skills. For the following, your task is to determine if the Tutor demonstrates the described quality at their specific point of progress in the conversation.
        </p>
        <p class="instruction">Go through the information and examples when it is your first time annotating this data!</p>

        {#each Array(5) as _, i}
            <div class="attribute">
                <div class="question-header">
                    <p>{i + 1}. {getQuestionText(i + 1)}</p>
                    <div class="button-group">
                        <button class="info-button" on:click={() => toggleInfo(i + 1)}>
                            {showInfo[i + 1] ? 'Hide Info' : 'More Info'}
                        </button>
                        <button class="example-button" on:click={() => toggleExamples(i + 1)}>
                            {showExamples[i + 1] ? 'Hide Examples' : 'Examples'}
                        </button>
                    </div>
                </div>
                {#if showInfo[i + 1]}
                    <pre class="info-box">
                        {getInfoText(i + 1)}
                        
                    </pre>
                {/if}
                {#if showExamples[i + 1]}
                    <div class="example-box">
                        {#each examples[i + 1] as example}
                            <div class="example">
                                <p><strong>Student:</strong> {example.Student}</p>
                                <p><strong>Tutor:</strong> {example.Tutor}</p>
                                <p><strong>Critic:</strong> {example.critic}</p>
                            </div>
                        {/each}
                    </div>
                {/if}
                <div class="rating-row">
                    <SelectButton 
                        bind:value={rubrics[i]} 
                        options={getOptions(i + 1)} 
                    />
                </div>
            </div>
        {/each}
    </div>
    <div class="button-container">
        <button on:click={submitRating} disabled={!isFormComplete}>Submit</button>
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
        cursor: not-allowed;
        color: #666;
    }
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .question-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .button-group {
        display: flex;
        gap: 10px;
    }
    .info-button, .example-button {
        background-color: #f0f0f0;
        color: #333;
        border: 1px solid #ccc;
        padding: 5px 10px;
        font-size: 14px;
        cursor: pointer;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .info-button:hover, .example-button:hover {
        background-color: #e0e0e0;
    }
    .info-box, .example-box {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        margin-top: 10px;
        font-size: 0.9em;
        text-wrap: wrap;
        font-family: Arial, Helvetica, sans-serif;
    }
    .student-status {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
        color: #856404;
    }

    .example {
        margin-bottom: 15px;
        padding-bottom: 15px;
        border-bottom: 1px solid #eee;
    }
    .example:last-child {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }
</style>

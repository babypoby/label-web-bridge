<form method="POST" action="?/login">
	<label>
		Email
		<input name="email" type="email" />
	</label>
	<label>
		Password
		<input name="password" type="password" />
	</label>
	<p class="error">Password must be at least 6 characters long.</p>
	<button>Login</button>
	<button formaction="?/signup">Sign up</button>
</form>


<style>
    .error {
        color: red;
        font-size: 0.8em;
    }
</style>
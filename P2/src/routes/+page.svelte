<script lang="ts">
	import Button from '$lib/components/ui/button/button.svelte';
	import Input from '$lib/components/ui/input/input.svelte';
	import Label from '$lib/components/ui/label/label.svelte';
	import Card from '$lib/components/ui/card/card.svelte';
	import {
		Root as Select,
		Trigger as SelectTrigger,
		Content as SelectContent,
		Item as SelectItem
	} from '$lib/components/ui/select';

	let formData = $state({
		cpu: '',
		gpu: '',
		ram: '',
		storage: '',
		os: '',
		genre: '',
		mode: '',
		age: '',
		budget: ''
	});

	const osOptions = ['Windows 10', 'Windows 11', 'macOS', 'Linux'];
	const ramOptions = ['4', '8', '16', '32'];
	const genreOptions = ['Action', 'RPG', 'Horror', 'Simulation'];
	const modeOptions = ['Singleplayer', 'Multiplayer', 'Co-op'];

	function handleSubmit() {
		console.log('Form Data:', formData);
		// TODO: Implementare la logica di query
	}
</script>

<div class="min-h-screen bg-gradient-to-br from-teal-50 to-cyan-50 p-8">
	<div class="mx-auto max-w-4xl">
		<!-- Header -->
		<div class="mb-12 text-center">
			<h1 class="mb-3 text-4xl font-bold text-teal-900">Game Matcher</h1>
			<p class="text-lg text-gray-600">
				Enter your specs to find games that run smoothly on your PC.
			</p>
		</div>

		<!-- Computer Specs Section -->
		<Card class="mb-8 bg-white p-8">
			<div class="mb-6">
				<h2 class="text-xl font-bold tracking-wide text-teal-600 uppercase">Computer Specs</h2>
			</div>
			<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
				<div>
					<Label for="cpu" class="mb-2 block">CPU</Label>
					<Input id="cpu" type="text" placeholder="e.g. AMD Ryzen 5" bind:value={formData.cpu} />
				</div>
				<div>
					<Label for="gpu" class="mb-2 block">GPU</Label>
					<Input
						id="gpu"
						type="text"
						placeholder="e.g. Nvidia GTX 1660"
						bind:value={formData.gpu}
					/>
				</div>
				<div>
					<Label for="ram" class="mb-2 block">RAM (GB)</Label>
					<Select type="single" bind:value={formData.ram}>
						<SelectTrigger id="ram" class="w-full">
							{#if formData.ram}
								{formData.ram} GB
							{:else}
								Select RAM...
							{/if}
						</SelectTrigger>
						<SelectContent>
							{#each ramOptions as option}
								<SelectItem value={option} label={`${option} GB`} />
							{/each}
						</SelectContent>
					</Select>
				</div>
				<div>
					<Label for="storage" class="mb-2 block">Available Storage (GB)</Label>
					<Input id="storage" type="number" placeholder="e.g. 100" bind:value={formData.storage} />
				</div>
				<div class="md:col-span-2">
					<Label for="os" class="mb-2 block">Operating System</Label>
					<Select type="single" bind:value={formData.os}>
						<SelectTrigger id="os" class="w-full">
							{#if formData.os}
								{formData.os}
							{:else}
								Select OS...
							{/if}
						</SelectTrigger>
						<SelectContent>
							{#each osOptions as option}
								<SelectItem value={option} label={option} />
							{/each}
						</SelectContent>
					</Select>
				</div>
			</div>
		</Card>

		<!-- Preferences Section -->
		<Card class="mb-8 bg-white p-8">
			<div class="mb-6">
				<h2 class="text-xl font-bold tracking-wide text-teal-600 uppercase">Preferences</h2>
			</div>
			<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
				<div>
					<Label for="genre" class="mb-2 block">Genre</Label>
					<Select type="single" bind:value={formData.genre}>
						<SelectTrigger id="genre" class="w-full">
							{#if formData.genre}
								{formData.genre}
							{:else}
								Select Genre...
							{/if}
						</SelectTrigger>
						<SelectContent>
							{#each genreOptions as option}
								<SelectItem value={option} label={option} />
							{/each}
						</SelectContent>
					</Select>
				</div>
				<div>
					<Label for="mode" class="mb-2 block">Player Mode</Label>
					<Select type="single" bind:value={formData.mode}>
						<SelectTrigger id="mode" class="w-full">
							{#if formData.mode}
								{formData.mode}
							{:else}
								Select Mode...
							{/if}
						</SelectTrigger>
						<SelectContent>
							{#each modeOptions as option}
								<SelectItem value={option} label={option} />
							{/each}
						</SelectContent>
					</Select>
				</div>
			</div>
		</Card>

		<!-- Personal & Budget Section -->
		<Card class="mb-8 bg-white p-8">
			<div class="mb-6">
				<h2 class="text-xl font-bold tracking-wide text-teal-600 uppercase">Personal & Budget</h2>
			</div>
			<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
				<div>
					<Label for="age" class="mb-2 block">Age</Label>
					<Input id="age" type="number" placeholder="Enter your age" bind:value={formData.age} />
				</div>
				<div>
					<Label for="budget" class="mb-2 block">Max Budget (€)</Label>
					<Input id="budget" type="number" placeholder="e.g. 50" bind:value={formData.budget} />
				</div>
			</div>
		</Card>

		<!-- Submit Button -->
		<div class="text-center">
			<Button onclick={handleSubmit}>MATCH MY PC</Button>
		</div>

		<!-- Results Area -->
		<div id="results" class="mt-12 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
			<!-- I risultati verranno aggiunti qui -->
		</div>
	</div>
</div>

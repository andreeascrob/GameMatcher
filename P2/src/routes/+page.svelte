<script lang="ts">
	import Button from '$lib/components/ui/button/button.svelte';
	import Input from '$lib/components/ui/input/input.svelte';
	import Label from '$lib/components/ui/label/label.svelte';
	import Card from '$lib/components/ui/card/card.svelte';
	import { Root as Select, Trigger as SelectTrigger, Content as SelectContent, Item as SelectItem } from '$lib/components/ui/select';

	let formData = $state({
		cpu: '',
		gpu: '',
		ram: '8',
		storage: '',
		os: 'Windows 10',
		genre: 'Action',
		mode: 'Singleplayer',
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
	<div class="max-w-4xl mx-auto">
		<!-- Header -->
		<div class="text-center mb-12">
			<h1 class="text-4xl font-bold text-teal-900 mb-3">Game Matcher</h1>
			<p class="text-gray-600 text-lg">Enter your specs to find games that run smoothly on your PC.</p>
		</div>

		<!-- Computer Specs Section -->
		<Card class="mb-8 bg-white p-8">
			<div class="mb-6">
				<h2 class="text-xl font-bold text-teal-600 uppercase tracking-wide">Computer Specs</h2>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				<div>
					<Label for="cpu" class="block mb-2">CPU</Label>
					<Input
						id="cpu"
						type="text"
						placeholder="e.g. AMD Ryzen 5"
						bind:value={formData.cpu}
					/>
				</div>
				<div>
					<Label for="gpu" class="block mb-2">GPU</Label>
					<Input
						id="gpu"
						type="text"
						placeholder="e.g. Nvidia GTX 1660"
						bind:value={formData.gpu}
					/>
				</div>
				<div>
					<Label for="ram" class="block mb-2">RAM (GB)</Label>
					<Select type="single" bind:value={formData.ram}>
						<SelectTrigger id="ram" class="w-full">
							{formData.ram} GB
						</SelectTrigger>
						<SelectContent>
							{#each ramOptions as option}
								<SelectItem value={option} label={`${option} GB`} />
							{/each}
						</SelectContent>
					</Select>
				</div>
				<div>
					<Label for="storage" class="block mb-2">Available Storage (GB)</Label>
					<Input
						id="storage"
						type="number"
						placeholder="e.g. 100"
						bind:value={formData.storage}
					/>
				</div>
				<div class="md:col-span-2">
					<Label for="os" class="block mb-2">Operating System</Label>
					<Select type="single" bind:value={formData.os}>
						<SelectTrigger id="os" class="w-full">
							{formData.os}
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
				<h2 class="text-xl font-bold text-teal-600 uppercase tracking-wide">Preferences</h2>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				<div>
					<Label for="genre" class="block mb-2">Genre</Label>
					<Select type="single" bind:value={formData.genre}>
						<SelectTrigger id="genre" class="w-full">
							{formData.genre}
						</SelectTrigger>
						<SelectContent>
							{#each genreOptions as option}
								<SelectItem value={option} label={option} />
							{/each}
						</SelectContent>
					</Select>
				</div>
				<div>
					<Label for="mode" class="block mb-2">Player Mode</Label>
					<Select type="single" bind:value={formData.mode}>
						<SelectTrigger id="mode" class="w-full">
							{formData.mode}
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
				<h2 class="text-xl font-bold text-teal-600 uppercase tracking-wide">Personal & Budget</h2>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				<div>
					<Label for="age" class="block mb-2">Age</Label>
					<Input
						id="age"
						type="number"
						placeholder="Enter your age"
						bind:value={formData.age}
					/>
				</div>
				<div>
					<Label for="budget" class="block mb-2">Max Budget (€)</Label>
					<Input
						id="budget"
						type="number"
						placeholder="e.g. 50"
						bind:value={formData.budget}
					/>
				</div>
			</div>
		</Card>

		<!-- Submit Button -->
		<div class="text-center">
			<Button
				onclick={handleSubmit}
			>
				MATCH MY PC
			</Button>
		</div>

		<!-- Results Area -->
		<div id="results" class="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
			<!-- I risultati verranno aggiunti qui -->
		</div>
	</div>
</div>

import { type Handle } from '@sveltejs/kit';
import { dev } from '$app/environment';
import { BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD } from '$env/static/private';

export const handle: Handle = async ({ event, resolve }) => {
	if (dev) {
		return resolve(event);
	}

	const authHeader = event.request.headers.get('authorization');

	if (!authHeader || !authHeader.startsWith('Basic ')) {
		return new Response('Unauthorized', {
			status: 401,
			headers: {
				'WWW-Authenticate': 'Basic realm="Protected Area"'
			}
		});
	}

	const credentials = atob(authHeader.slice(6));
	const [username, password] = credentials.split(':');

	if (username !== BASIC_AUTH_USERNAME || password !== BASIC_AUTH_PASSWORD) {
		return new Response('Unauthorized', {
			status: 401,
			headers: {
				'WWW-Authenticate': 'Basic realm="Protected Area"'
			}
		});
	}

	return resolve(event);
};

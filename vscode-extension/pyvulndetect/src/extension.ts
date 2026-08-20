import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {

	const disposable = vscode.commands.registerCommand('pyvulndetect.scan', async () => {
		const editor = vscode.window.activeTextEditor;
		if (!editor) {
			vscode.window.showErrorMessage('No active editor found');
			return;
		}

		const code = editor.document.getText();

		try {
			const response = await fetch('http://127.0.0.1:8000/predict', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ code: code }),
			});

			const result = await response.json() as { prediction: string; confidence: number };

			vscode.window.showInformationMessage(
				`${result.prediction} (${(result.confidence * 100).toFixed(0)}% confidence)`
			);

		} catch (error) {
			vscode.window.showErrorMessage('Could not connect to PyVulnDetect server. Is it running?');
		}
	});

	context.subscriptions.push(disposable);
}

export function deactivate() {}
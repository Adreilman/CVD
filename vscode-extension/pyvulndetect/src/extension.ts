import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {

	const diagnosticCollection = vscode.languages.createDiagnosticCollection('pyvulndetect');
	context.subscriptions.push(diagnosticCollection);

	const disposable = vscode.commands.registerCommand('pyvulndetect.scan', async () => {
		const editor = vscode.window.activeTextEditor;
		if (!editor) {
			vscode.window.showErrorMessage('No active editor found');
			return;
		}

		const code = editor.document.getText();
		vscode.window.showInformationMessage('PyVulnDetect: Scanning...');

		try {
			const response = await fetch('http://127.0.0.1:8000/predict', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ code: code }),
			});

			const result = await response.json() as { prediction: string; confidence: number };
			const confidence = result.confidence;
			const prediction = result.prediction;

			diagnosticCollection.clear();

			if (prediction !== 'Safe' && confidence >= 0.75) {
				const range = new vscode.Range(
					new vscode.Position(0, 0),
					new vscode.Position(editor.document.lineCount - 1, 0)
				);
				const diagnostic = new vscode.Diagnostic(
					range,
					`⚠️ ${prediction} detected (${(confidence * 100).toFixed(0)}% confidence)`,
					vscode.DiagnosticSeverity.Warning
				);
				diagnosticCollection.set(editor.document.uri, [diagnostic]);
			}

			vscode.window.showInformationMessage(
				`${prediction} (${(confidence * 100).toFixed(0)}% confidence)`
			);

		} catch (error) {
			vscode.window.showErrorMessage('Could not connect to PyVulnDetect server. Is it running?');
		}
	});

	context.subscriptions.push(disposable);
}

export function deactivate() {}
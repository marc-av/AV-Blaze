// Default snippets to load on first run
const defaultSnippets = {
    "/ja": "Hi Peter! I wanted to try to get a hold of you before your phone starts getting blown up by sales agents, I figured a text would work best, I hope I’m not too late￼   My name’s Jonathan, I am a Healthcare Advisor for FL. Your information just came across my desk that you’re looking for health coverage. I’m here to help, I have a certain license that gives me access to every plan available in the State. I’m sure you’re very busy. May I ask you some questions through text so I can send you quotes? Or would you rather setup an appointment to go over your options?"
};

let snippets = {};

function loadSnippets() {
    // Using v2 key to bust old cache and force load from new defaultSnippets
    const saved = localStorage.getItem('tb_snippets_v2');
    if (saved) {
        try {
            snippets = JSON.parse(saved);
        } catch(e) {
            snippets = {...defaultSnippets};
        }
    } else {
        snippets = {...defaultSnippets};
        saveSnippets();
    }
}

function saveSnippets() {
    localStorage.setItem('tb_snippets_v2', JSON.stringify(snippets));
}

// UI Elements
const editor = document.getElementById('editor');
const snippetList = document.getElementById('snippet-list');

// Prompt Modal Logic
const promptModalOverlay = document.getElementById('prompt-modal-overlay');
const promptTitle = document.getElementById('prompt-title');
const promptDesc = document.getElementById('prompt-desc');
const promptInput = document.getElementById('prompt-input');
const promptSubmit = document.getElementById('prompt-submit');
const promptCancel = document.getElementById('prompt-cancel');

function customPrompt(title, desc) {
    return new Promise((resolve) => {
        promptTitle.textContent = title;
        promptDesc.textContent = desc;
        promptInput.value = '';
        
        promptModalOverlay.classList.add('active');
        promptInput.focus();
        
        const cleanup = () => {
            promptModalOverlay.classList.remove('active');
            promptSubmit.removeEventListener('click', onSubmit);
            promptCancel.removeEventListener('click', onCancel);
            promptInput.removeEventListener('keydown', onKeydown);
            editor.focus();
        };

        const onSubmit = () => {
            const val = promptInput.value;
            cleanup();
            resolve(val);
        };

        const onCancel = () => {
            cleanup();
            resolve(""); 
        };

        const onKeydown = (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                onSubmit();
            } else if (e.key === 'Escape') {
                e.preventDefault();
                onCancel();
            }
        };

        promptSubmit.addEventListener('click', onSubmit);
        promptCancel.addEventListener('click', onCancel);
        promptInput.addEventListener('keydown', onKeydown);
    });
}

// Snippet Editor Modal Logic
const snippetModalOverlay = document.getElementById('snippet-modal-overlay');
const snippetModalTitle = document.getElementById('snippet-modal-title');
const snippetTriggerInput = document.getElementById('snippet-trigger-input');
const snippetContentInput = document.getElementById('snippet-content-input');
const snippetSubmit = document.getElementById('snippet-submit');
const snippetCancel = document.getElementById('snippet-cancel');
const btnAddSnippet = document.getElementById('btn-add-snippet');

let editingTrigger = null; // if null, we are adding

function openSnippetModal(trigger = null) {
    editingTrigger = trigger;
    if (trigger) {
        snippetModalTitle.textContent = 'Edit Snippet';
        snippetTriggerInput.value = trigger;
        snippetContentInput.value = snippets[trigger];
    } else {
        snippetModalTitle.textContent = 'Add Snippet';
        snippetTriggerInput.value = '/';
        snippetContentInput.value = '';
    }
    
    snippetModalOverlay.classList.add('active');
    snippetTriggerInput.focus();
}

function closeSnippetModal() {
    snippetModalOverlay.classList.remove('active');
}

snippetCancel.addEventListener('click', closeSnippetModal);
btnAddSnippet.addEventListener('click', () => openSnippetModal(null));

snippetSubmit.addEventListener('click', () => {
    let newTrigger = snippetTriggerInput.value.trim();
    const newContent = snippetContentInput.value;
    
    if (!newTrigger) {
        alert("Trigger cannot be empty.");
        return;
    }
    
    // Auto prefix slash if missing
    if (!newTrigger.startsWith('/')) {
        newTrigger = '/' + newTrigger;
    }

    if (!newContent) {
        alert("Content cannot be empty.");
        return;
    }

    // Check for duplicates
    if (editingTrigger !== newTrigger && snippets[newTrigger]) {
        alert("A snippet with this trigger already exists.");
        return;
    }

    // Delete old if trigger changed
    if (editingTrigger && editingTrigger !== newTrigger) {
        delete snippets[editingTrigger];
    }

    snippets[newTrigger] = newContent;
    saveSnippets();
    renderSnippets();
    closeSnippetModal();
});

// Sidebar Rendering
function renderSnippets() {
    snippetList.innerHTML = '';
    
    // Sort by trigger
    const sortedTriggers = Object.keys(snippets).sort();

    for (const trigger of sortedTriggers) {
        const content = snippets[trigger];
        const div = document.createElement('div');
        div.className = 'snippet';
        div.innerHTML = `
            <div class="snippet-header">
                <span class="trigger">${trigger}</span>
                <div class="snippet-actions">
                    <button class="btn-icon btn-edit" title="Edit">✏️</button>
                    <button class="btn-icon danger btn-delete" title="Delete">🗑️</button>
                </div>
            </div>
            <div class="snippet-content">${content}</div>
        `;
        
        // Event Listeners for Edit/Delete
        div.querySelector('.btn-edit').addEventListener('click', () => {
            openSnippetModal(trigger);
        });
        
        div.querySelector('.btn-delete').addEventListener('click', () => {
            if (confirm(`Are you sure you want to delete ${trigger}?`)) {
                delete snippets[trigger];
                saveSnippets();
                renderSnippets();
            }
        });

        snippetList.appendChild(div);
    }
}

// Engine state
let isExpanding = false;

// Trigger Detection & Execution
editor.addEventListener('input', async (e) => {
    if (isExpanding) return;

    const text = editor.value;
    const cursorPosition = editor.selectionStart;

    // Check if the text right before the cursor matches any trigger
    for (const trigger of Object.keys(snippets)) {
        if (text.substring(cursorPosition - trigger.length, cursorPosition) === trigger) {
            
            isExpanding = true;
            
            const template = snippets[trigger];
            const expandedText = await executeTemplate(template);
            
            const beforeTrigger = text.substring(0, cursorPosition - trigger.length);
            const afterTrigger = text.substring(cursorPosition);
            
            editor.value = beforeTrigger + expandedText + afterTrigger;
            
            editor.selectionStart = editor.selectionEnd = beforeTrigger.length + expandedText.length;
            
            isExpanding = false;
            break; 
        }
    }
});

// The core execution engine resolving variables and forms
async function executeTemplate(template) {
    let result = template;
    const localVars = {}; 

    const pattern = /\{([a-z]+):([^}]+)\}/g;
    const matches = [...template.matchAll(pattern)];
    
    for (const match of matches) {
        const fullMatch = match[0];
        const type = match[1];
        const name = match[2];
        
        let replacementValue = "";

        if (type === 'form') {
            if (localVars[name] === undefined) {
                const userInput = await customPrompt('Form Input Required', `Please provide a value for: ${name}`);
                localVars[name] = userInput || "";
            }
            replacementValue = localVars[name];
        } 
        else if (type === 'var') {
            replacementValue = localVars[name] || "";
        }
        else if (type === 'store') {
            const userInput = await customPrompt('Persistent Input Required', `Please provide a value to store for: ${name}`);
            localStorage.setItem(`tb_var_${name}`, userInput || "");
            replacementValue = userInput || "";
        }
        else if (type === 'recall') {
            replacementValue = localStorage.getItem(`tb_var_${name}`) || "";
        }
        else if (type === 'func') {
            if (name === 'todayDate') {
                replacementValue = new Date().toLocaleDateString();
            }
        }

        result = result.replace(fullMatch, replacementValue);
    }

    return result;
}

// Startup
loadSnippets();
renderSnippets();

const fs = require('fs');
const path = require('path');

const srcBase = path.resolve('.claude/skills/anthropics/skills');
const destBase = path.resolve('.claude/skills');

console.log(`Source: ${srcBase}`);
console.log(`Dest: ${destBase}`);

if (fs.existsSync(srcBase)) {
    const skills = fs.readdirSync(srcBase);
    skills.forEach(skill => {
        const srcPath = path.join(srcBase, skill);
        const destPath = path.join(destBase, skill);
        
        // Skip if destination already exists
        if (fs.existsSync(destPath)) {
            console.log(`Skipping ${skill} (already exists)`);
            return;
        }

        try {
            const stat = fs.statSync(srcPath);
            if (stat.isDirectory()) {
                console.log(`Moving ${skill}...`);
                fs.renameSync(srcPath, destPath);
            }
        } catch (e) {
            console.error(`Error moving ${skill}: ${e.message}`);
        }
    });
    console.log('Done moving skills.');
} else {
    console.log('Source directory not found.');
}

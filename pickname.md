
## Random name pick

You can copy this file and save as html after changing the list of the name below

```html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>High-Drama Name Picker</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #1a1a1a; /* Darker theme for more drama */
            overflow: hidden;
        }
        .container {
            text-align: center;
            background-color: #2c2c2c;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            border: 1px solid #444;
            width: 90%;
            max-width: 700px;
            transition: transform 0.2s ease-in-out;
        }
        .container.picking {
            animation: shake 0.5s ease-in-out infinite alternate;
        }
        @keyframes shake {
            from { transform: scale(1) rotate(-0.5deg); }
            to { transform: scale(1.02) rotate(0.5deg); }
        }
        h1 {
            color: #e0e0e0;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 0 0 10px rgba(255, 165, 0, 0.5);
        }
        #pickedName {
            font-size: 2em;
            font-weight: bold;
            color: #ffa500; /* Orange for emphasis */
            min-height: 60px;
            margin-bottom: 30px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow-wrap: break-word;
            word-break: break-word;
            padding: 10px;
            border: 2px dashed #555;
            border-radius: 10px;
            transition: all 0.1s;
        }
        #pickedName.celebrate {
            border-style: solid;
            border-color: #ffd700;
            color: #ffd700;
            text-shadow: 0 0 15px #ffd700;
            animation: big-reveal 0.8s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        }
        @keyframes big-reveal {
            0% { transform: scale(0.5); opacity: 0.5; }
            50% { transform: scale(1.25); opacity: 1; }
            100% { transform: scale(1.1); opacity: 1; }
        }
        button {
            background: linear-gradient(145deg, #ff4b2b, #ff416c);
            color: white;
            border: none;
            padding: 18px 35px;
            font-size: 1.2em;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 5px 15px rgba(255, 65, 108, 0.4);
        }
        button:hover:not(:disabled) {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 25px rgba(255, 65, 108, 0.6);
        }
        button:active:not(:disabled) {
            transform: translateY(0) scale(1);
        }
        button:disabled {
            background: #555;
            cursor: not-allowed;
            box-shadow: none;
        }
        .confetti-piece {
            position: absolute;
            width: 10px;
            height: 20px;
            background-color: #f0f;
            opacity: 0;
            animation: confetti-burst 3s ease-out forwards;
        }
        @keyframes confetti-burst {
            0% { transform: translate(0, 0) rotate(0deg); opacity: 1; }
            100% { transform: translate(var(--x), var(--y)) rotate(var(--rot)); opacity: 0; }
        }
    </style>
</head>
<body>

    <div class="container" id="container">
        <h1>THE DECIDER</h1>
        <div id="pickedName">Your Destiny Awaits...</div>
        <button id="pickButton" onclick="startPicking()">Unleash Fate!</button>
    </div>

    <script>
        const names = [
            "WAN MUHAMMAD ADLI BIN WAN MUHAMMAD SUKRI", "MUHD ALIFF FITRI BIN NIRWAN", "OOI CHOON HAN", "JASON LEE TIAN TECK", "NURUL NAJWA BINTI MOHD HASHIM", "MEILIN LI", "NUR IMAN HAZWAN BIN SAHIDAN", "XIA LIPING", "NUR BASYIRAH BINTI SAUFI", "WAN NUR SYAMIMI BINTI WAN AFFANDI", "AINUL MARDHIAH BINTI CHAHURI", "KOH XIAO XUEN", "MA RONG", "CHANG KAH KIEN", "NURFATIN ALISA BINTI MUZAHAIRIL", "ZHOU XINPEI", "MUHAMMAD EIDLAN BIN MOHD NOR AMIRUDDIN", "HARITH RAZIQIN BIN KHALIL", "QAMARINA BINTI AMRAN", "ZHOUYAN", "RORAINE CELESTE ANAK RONALD", "NGAI CHOONG MING", "NAQIYYATUL AILEEN KARMILA BINTI NAZRI", "HAJAR BINTI AZMIN BASYA", "SUHAILA BINTI MAT HASSAN", "CATHERINE IRYSTA ANAK JOHUA", "CAROL CHIN YONG EN", "MUHAMMAD AKMAL IZZ BIN SULAIMAN", "NAHGAJOTHY A/P KARUNAKARAN", "FENG YIXUAN", "NUR AIQA ALYSHA BINTI MOHD ZAIN", "FARAH SYAHMINA HAZIQAH BINTI SHARIPUDDIN", "TAN WEI KAI", "ONG THENG YIK", "MUHAMMAD ZARIF BIN SAIFUL HAFIZI", "LIM SEI HOE", "SOFIA BINTI RAHIM", "NURUL FATIHAH BINTI NAZRI", "NUR SAIDATUL AFIQAH BINTI RAMLI", "YANG JINLONG", "ZAHRA", "NIK SABRINA NATEESHA BINTI KAMAL ZAHARI", "NOR FAZIRAH BINTI MOHD ANUAR", "FOONG YIN KEI", "TAN KAI ZHE", "NURINA ATIQAH BINTI SHAHRUDIN", "ALEYA NADIRA BINTI MOHD AMRAN", "LUQMANULHAKIM BIN MATRABI", "ZHANG ZHIHENG", "NURRASHIDAH BINTI WADZER", "XIAO YUTONG", "HANA HUMAIRA BINTI HENDRY", "WANG YUMO", "AS-SHUHADA BINTI AHMADE", "SOFIYYA KHADEEJA BINTI HASAHUDIN", "RACHEL DAVID", "SITI NUR QASRINA BINTI ABD HAMID", "VANIA JOHN PEREIRA", "NUR ANIS DANIA BINTI MOHD FAUZI", "YANG HAORUI", "MUIZZUDIN", "MUHAMMAD ALIF BIN MOHAMAD SHUKRI", "MUHAMMAD HAIKAL BIN SAIPUL AMRI", "LIN JOON QY", "XIEMENGTING", "NUHA BINTI MOHAMAD NASER", "CHEAH ZHAN SEN", "NUR ATHIRAH BINTI MOHAMAD RUZAMAN", "NOR ALIA SAFIYYA BINTI MOHD FAZLI", "MUHAMMAD DANIAL BIN ZAINUDIN", "SAFIYAH AZRIANA BINTI AZMI", "NUR IZZAH BAHYAH BINTI MOHD ESHAM", "NUR DAMIA BINTI MOHAMAD ZAIDI", "MUHAMMAD ZAIM BIN KAMAROL RIDZUAN", "HASANAL BIN MOHAMMAD SUNSI", "WANG JIN", "FATEEN ZULAIKHA BINTI HAZLI", "MALIKA ZAINAB BINTI ABDULLAH", "NUR NAFISYAH NADIA BINTI KHAIRUDDIN", "NUR SYAZLINDA BINTI HASMI", "SONG JIAXIN", "NUR MIRZA DAYINI BINTI FAIZUL AZLANI", "WAN CHENG", "CAO YE", "ERISYA KAMALIA BINTI MOHAMAD MOHSIN", "NUR ALIA BINTI EFFENDY @ ZAMIRRUDIN", "KARMILA AYU BINTI SAIFUL BAHRI", "IQBAL HAKKIMI BIN NOR HISHAM", "SOFEA BINTI AHMAD FAIZ", "AMIR SYAHMI BIN AHMAD HAIRIDAN", "ZHANG CHAOKAI", "CHEN GUO", "NUR ELISA SUHAILA BINTI AYOB", "MESHALEE A/P KRISHNAMURTHY", "SAIDATUL AZLIN BINTI SAIDIN", "MUHAMMAD NAUFAL BIN MOHD ZULKIFLI", "MUHAMMAD FARKHAN BIN SERU AZAM", "SITI AISYAH BINTI MAHAMUD", "LEONG XUAN YAO", "NUR SAFI BALQIS BINTI AMRAN", "DANIAL ARIFFIN BIN ABU BAKAR", "MUHAMMAD IHSAN BIN IDRUS"
        ];

        const pickedNameElement = document.getElementById('pickedName');
        const pickButton = document.getElementById('pickButton');
        const container = document.getElementById('container');
        let audioContext;
        let nameFlashInterval;

        // Initialize AudioContext on first user interaction
        const initAudio = () => {
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }
        };
        
        // --- Sound Generation ---
        const playTickSound = () => {
            if (!audioContext) return;
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.type = 'triangle';
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.0001, audioContext.currentTime + 0.05);
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.05);
        };

        const playSuccessSound = () => {
            if (!audioContext) return;
            const notes = [392.00, 523.25, 659.25, 783.99]; // G4, C5, E5, G5
            notes.forEach((freq, i) => {
                const osc = audioContext.createOscillator();
                const gain = audioContext.createGain();
                osc.connect(gain);
                gain.connect(audioContext.destination);
                
                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, audioContext.currentTime + i * 0.1);
                gain.gain.setValueAtTime(0.2, audioContext.currentTime + i * 0.1);
                gain.gain.exponentialRampToValueAtTime(0.0001, audioContext.currentTime + i * 0.1 + 0.2);
                osc.start(audioContext.currentTime + i * 0.1);
                osc.stop(audioContext.currentTime + i * 0.1 + 0.2);
            });
        };

        const startPicking = () => {
            initAudio(); // Ensure audio is ready
            pickButton.disabled = true;
            pickedNameElement.classList.remove('celebrate');
            container.classList.add('picking');

            // Rapidly flash names
            nameFlashInterval = setInterval(() => {
                const randomName = names[Math.floor(Math.random() * names.length)];
                pickedNameElement.textContent = randomName;
                playTickSound();
            }, 60); // Flash names every 60ms

            // After 1 second, stop flashing and reveal the winner
            setTimeout(revealWinner, 1000);
        };

        const revealWinner = () => {
            clearInterval(nameFlashInterval);
            container.classList.remove('picking');

            const winner = names[Math.floor(Math.random() * names.length)];
            pickedNameElement.textContent = winner;
            pickedNameElement.classList.add('celebrate');
            
            playSuccessSound();
            createConfetti();

            setTimeout(() => {
                pickButton.disabled = false;
            }, 1500); // Re-enable button after celebration
        };

        function createConfetti() {
            const colors = ['#ffd700', '#ff8c00', '#ff4500', '#ffffff', '#ff69b4'];
            const numberOfConfetti = 100;
            const container = document.body;

            for (let i = 0; i < numberOfConfetti; i++) {
                const confetti = document.createElement('div');
                confetti.classList.add('confetti-piece');
                confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                
                const startX = window.innerWidth / 2;
                const startY = window.innerHeight / 2;
                confetti.style.left = `${startX}px`;
                confetti.style.top = `${startY}px`;

                const targetX = (Math.random() - 0.5) * window.innerWidth * 1.5;
                const targetY = (Math.random() - 0.5) * window.innerHeight * 1.5;
                const rotation = Math.random() * 1080 - 540;

                confetti.style.setProperty('--x', `${targetX}px`);
                confetti.style.setProperty('--y', `${targetY}px`);
                confetti.style.setProperty('--rot', `${rotation}deg`);

                container.appendChild(confetti);

                confetti.addEventListener('animationend', () => {
                    confetti.remove();
                });
            }
        }
    </script>

```

</body>

</html>


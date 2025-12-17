window.addEventListener('load', () => {
    const aiSegment = document.querySelector('.donut-segment-ai');
    const humanSegment = document.querySelector('.donut-segment-human');

    const radius = 72;
    const circumference = 2 * Math.PI * radius;

    const aiDash = (AI_PERCENT / 100) * circumference;
    const humanDash = (HUMAN_PERCENT / 100) * circumference;

    aiSegment.style.strokeDasharray = `${aiDash} ${circumference}`;
    humanSegment.style.strokeDasharray = `${humanDash} ${circumference}`;
    humanSegment.style.strokeDashoffset = -aiDash;
});
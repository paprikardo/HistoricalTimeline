import React, { useState, useRef, useEffect } from 'react';
import CollapsibleEventCard from './CollapsibleEventCard';
import './Events.css';

const ZoomableTimeline = () => {
    const containerRef = useRef(null);
    const [scrollLeft, setScrollLeft] = useState(0);
    //events is an array of dictonaries with the following keys: id, name, description, time_informal, year, relevance
    const [events, setEvents] = useState([]); // Initialize the events state to an empty array [
    const [from_year, setFromYear] = useState(1980);
    const [to_year, setToYear] = useState(2022);
    // Use the useEffect hook to fetch events when the component mounts
    useEffect(() => {
        // Define a function to fetch events from your API
        const fetchEvents = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/');
                if (response.ok) {
                    const data = await response.json();
                    setEvents(data); // Set the events data in the state
                } else {
                    console.error('Failed to fetch events');
                }
            } catch (error) {
                console.error('Error fetching events:', error);
            }
        };

        fetchEvents(); // Call the fetchEvents function when the component mounts
    }, []);

    const handleScroll = (event) => {
        const scrollDelta = event.deltaY || event.detail || event.wheelDelta;

        // Calculate the cursor's position as a percentage within the timeline div
        const container = containerRef.current;
        const cursorX = event.clientX - container.getBoundingClientRect().left;
        const containerWidth = container.offsetWidth;
        const cursorPosition = (cursorX / containerWidth) * 100;

        // Calculate the adjustment based on the cursor position
        const adjustment = (to_year - from_year) * (scrollDelta > 0 ? -0.01 : 0.01);
        // Adjust from_year and to_year based on the cursor position and zoom direction
        setFromYear(from_year + adjustment * cursorPosition / 100);
        setToYear(to_year - adjustment * (100 - cursorPosition) / 100);

        // Adjust the scrollLeft position of the container based on the scroll direction.
        setScrollLeft((prevScrollLeft) => prevScrollLeft + scrollDelta);
    };


    const calculateCardPosition = (eventYear) => {
        const totalYearsInRange = to_year - from_year;
        const cardPosition = ((eventYear - from_year) / totalYearsInRange) * 100;
        return cardPosition + '%';
    };

    return (
        <div
            className="timeline-container"
            ref={containerRef}
            onWheel={handleScroll}
        >
            <p>Shown are events from year {Math.round(from_year)} to year {Math.round(to_year)}</p>
            <div className="timeline">
                {events.map((event) => {
                    if (event.year < from_year || event.year > to_year) return <></>;
                    const cardPosition = calculateCardPosition(event.year);
                    return <CollapsibleEventCard style={{ left: cardPosition }}
                        collapsed={false} I
                        key={event.id} event={event} />;
                }
                )}
            </div>
        </div>
    );
};

export default ZoomableTimeline;

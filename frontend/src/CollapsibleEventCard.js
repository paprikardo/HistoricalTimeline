import React from 'react';

const CollapsibleEventCard = ({ collapsed, event, style}) => {
  return (
    <div style={style} className={`${collapsed ? 'collapsed' : 'event-card'}`}>
      {!collapsed && (
        <>
          <div className="event-card-name">{event.name}</div>
          <div className="event-card-time">{event.time_informal}</div>
          <div className="event-card-description">{event.description}</div>
        </>
      )}
    </div>
  );
};

export default CollapsibleEventCard;

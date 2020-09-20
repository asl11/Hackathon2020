import React from 'react'

export default ({ skillnames }) => {
  return (
      skillnames.map((name, index) =>
        <div class="progress">
          <span class="skill">{name}</span>
        </div>
      )

  )

}

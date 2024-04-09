on run {targetBuddyPhone, targetMessage}
    tell application "Messages"
        send targetMessage to buddy targetBuddyPhone of (service 1 whose service type is iMessage)
    end tell
end run
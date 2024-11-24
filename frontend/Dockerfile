# Use Ubuntu as the base image
FROM ubuntu:22.04
# Set environment variables to prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
# Install Node.js and necessary tools
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# Set the working directory
WORKDIR /app
# Copy package.json and package-lock.json
COPY package*.json ./
# Install dependencies
RUN npm install
# Copy the rest of the application code
COPY . .
# Build the application for production
RUN npm run build
# Expose the Vite preview port (4173 by default)
EXPOSE 4173
# Command to run the Vite preview server
CMD ["npm", "run", "preview","--host 0.0.0.0"]
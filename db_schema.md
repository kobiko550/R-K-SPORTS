# FitHarmony NeonDB Database Schema

Below is the complete database design for FitHarmony, featuring raw SQL DDL and modern JavaScript-based **Drizzle ORM** schemas.

---

## 1. Drizzle ORM Schema (`db/schema.js`)

```javascript
import { pgTable, uuid, text, varchar, timestamp, integer, doublePrecision, boolean, date } from 'drizzle-orm/pg-core';

// 1. Users Table
export const users = pgTable('users', {
  id: uuid('id').defaultRandom().primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  passwordHash: text('password_hash'), // Nullable for OAuth users
  googleId: varchar('google_id', { length: 255 }).unique(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});

// 2. Profiles Table
export const profiles = pgTable('profiles', {
  id: uuid('id').defaultRandom().primaryKey(),
  userId: uuid('user_id').references(() => users.id, { onDelete: 'cascade' }).notNull().unique(),
  fullName: varchar('full_name', { length: 255 }).notNull(),
  gender: varchar('gender', { length: 10 }).notNull(), // 'male' | 'female'
  age: integer('age').notNull(),
  weight: doublePrecision('weight').notNull(), // in kg
  height: doublePrecision('height').notNull(), // in cm
  activityLevel: varchar('activity_level', { length: 50 }).notNull(), // 'sedentary' | 'light' | 'moderate' | 'active' | 'extreme'
  goal: varchar('goal', { length: 50 }).notNull(), // 'lose' | 'maintain' | 'gain'
  bmr: doublePrecision('bmr').notNull(),
  tdee: doublePrecision('tdee').notNull(),
  language: varchar('language', { length: 5 }).default('he').notNull(), // 'he' | 'en'
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});

// 3. Daily Nutrition Logs Table
export const dailyLogs = pgTable('daily_logs', {
  id: uuid('id').defaultRandom().primaryKey(),
  userId: uuid('user_id').references(() => users.id, { onDelete: 'cascade' }).notNull(),
  logDate: date('log_date').defaultNow().notNull(),
  mealType: varchar('meal_type', { length: 50 }).notNull(), // 'breakfast' | 'lunch' | 'dinner' | 'snack'
  foodName: varchar('food_name', { length: 255 }).notNull(),
  calories: integer('calories').notNull(),
  protein: doublePrecision('protein').default(0).notNull(),
  carbs: doublePrecision('carbs').default(0).notNull(),
  fat: doublePrecision('fat').default(0).notNull(),
  imageUrl: text('image_url'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

// 4. Workouts Table
export const workouts = pgTable('workouts', {
  id: uuid('id').defaultRandom().primaryKey(),
  userId: uuid('user_id').references(() => users.id, { onDelete: 'cascade' }).notNull(),
  workoutDate: date('workout_date').defaultNow().notNull(),
  activityType: varchar('activity_type', { length: 100 }).notNull(), // e.g., 'Running', 'Strength Training'
  durationMinutes: integer('duration_minutes').notNull(),
  caloriesBurned: integer('calories_burned').notNull(),
  source: varchar('source', { length: 50 }).default('manual').notNull(), // 'manual' | 'apple_health' | 'google_fit' | 'garmin'
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

// 5. Smartwatch Sync Logs & Settings Table
export const smartwatchSync = pgTable('smartwatch_sync', {
  id: uuid('id').defaultRandom().primaryKey(),
  userId: uuid('user_id').references(() => users.id, { onDelete: 'cascade' }).notNull().unique(),
  provider: varchar('provider', { length: 50 }).notNull(), // 'apple_health' | 'google_fit' | 'garmin' | 'samsung'
  accessToken: text('access_token'),
  refreshToken: text('refresh_token'),
  lastSyncTime: timestamp('last_sync_time'),
  syncStatus: varchar('sync_status', { length: 50 }).default('active').notNull(), // 'active' | 'expired' | 'error'
  createdAt: timestamp('created_at').defaultNow().notNull(),
});
```

---

## 2. Raw SQL DDL (PostgreSQL)

```sql
-- Create USERS Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT,
    google_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create PROFILES Table
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('male', 'female')),
    age INT NOT NULL,
    weight DOUBLE PRECISION NOT NULL,
    height DOUBLE PRECISION NOT NULL,
    activity_level VARCHAR(50) NOT NULL CHECK (activity_level IN ('sedentary', 'light', 'moderate', 'active', 'extreme')),
    goal VARCHAR(50) NOT NULL CHECK (goal IN ('lose', 'maintain', 'gain')),
    bmr DOUBLE PRECISION NOT NULL,
    tdee DOUBLE PRECISION NOT NULL,
    language VARCHAR(5) DEFAULT 'he' NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create DAILY_LOGS Table
CREATE TABLE daily_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    log_date DATE DEFAULT CURRENT_DATE NOT NULL,
    meal_type VARCHAR(50) NOT NULL CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
    food_name VARCHAR(255) NOT NULL,
    calories INT NOT NULL,
    protein DOUBLE PRECISION DEFAULT 0 NOT NULL,
    carbs DOUBLE PRECISION DEFAULT 0 NOT NULL,
    fat DOUBLE PRECISION DEFAULT 0 NOT NULL,
    image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create WORKOUTS Table
CREATE TABLE workouts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    workout_date DATE DEFAULT CURRENT_DATE NOT NULL,
    activity_type VARCHAR(100) NOT NULL,
    duration_minutes INT NOT NULL,
    calories_burned INT NOT NULL,
    source VARCHAR(50) DEFAULT 'manual' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create SMARTWATCH_SYNC Table
CREATE TABLE smartwatch_sync (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL CHECK (provider IN ('apple_health', 'google_fit', 'garmin', 'samsung')),
    access_token TEXT,
    refresh_token TEXT,
    last_sync_time TIMESTAMP WITH TIME ZONE,
    sync_status VARCHAR(50) DEFAULT 'active' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```
